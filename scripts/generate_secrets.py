#!/usr/bin/env python3
"""
Cryptographically secure secret generator for Atena DevSecOps environment.
Generates isolated secrets in .secrets/ directory for Docker Secrets and local deployment.
"""

import secrets
import string
from pathlib import Path


def generate_secure_password(length=32):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_django_secret_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(chars) for _ in range(50))


def main():
    repo_root = Path(__file__).resolve().parent.parent
    secrets_dir = repo_root / '.secrets'
    secrets_dir.mkdir(parents=True, exist_ok=True)

    db_user = "atena_app"
    db_name = "atena_prod"
    db_password = generate_secure_password(32)
    django_secret = generate_django_secret_key()
    database_url = f"postgres://{db_user}:{db_password}@atena-postgres:5432/{db_name}"

    files_to_write = {
        'postgres_db.txt': db_name,
        'postgres_user.txt': db_user,
        'postgres_password.txt': db_password,
        'django_secret_key.txt': django_secret,
        'database_url.txt': database_url,
    }

    for filename, content in files_to_write.items():
        file_path = secrets_dir / filename
        file_path.write_text(content.strip(), encoding='utf-8')
        try:
            # Set POSIX permissions 600 (owner read/write only)
            file_path.chmod(0o600)
        except Exception:
            pass

    print(f"[*] [DevSecOps] Successfully generated secure secrets in: {secrets_dir}")
    print("   -> postgres_db.txt")
    print("   -> postgres_user.txt")
    print("   -> postgres_password.txt")
    print("   -> django_secret_key.txt")
    print("   -> database_url.txt")
    print("[!] Never commit the .secrets/ folder to version control.")


if __name__ == '__main__':
    main()
