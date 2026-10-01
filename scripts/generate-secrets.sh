#!/usr/bin/env bash
# Generates isolated, cryptographically strong secrets in .secrets/ directory
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "${SCRIPT_DIR}")"
SECRETS_DIR="${REPO_ROOT}/.secrets"

mkdir -p "${SECRETS_DIR}"

if command -v python3 >/dev/null 2>&1; then
    python3 "${SCRIPT_DIR}/generate_secrets.py"
else
    # Fallback using openssl if Python is unavailable
    echo "atena_prod" > "${SECRETS_DIR}/postgres_db.txt"
    echo "atena_app" > "${SECRETS_DIR}/postgres_user.txt"
    openssl rand -base64 24 | tr -dc 'a-zA-Z0-9' | head -c 32 > "${SECRETS_DIR}/postgres_password.txt"
    openssl rand -base64 36 | tr -dc 'a-zA-Z0-9!@#$%^&*(-_=+)' | head -c 50 > "${SECRETS_DIR}/django_secret_key.txt"
    
    DB_PASS=$(cat "${SECRETS_DIR}/postgres_password.txt")
    echo "postgres://atena_app:${DB_PASS}@atena-postgres:5432/atena_prod" > "${SECRETS_DIR}/database_url.txt"
    
    chmod 600 "${SECRETS_DIR}"/*
    echo "🔒 [DevSecOps] Generated secrets using OpenSSL in ${SECRETS_DIR}"
fi
