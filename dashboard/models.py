from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

#Classe para que o Django reconheça o email como campo de login
class UserManager(BaseUserManager):
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

# Classe de usuário personalizada
class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    username = None
    role = models.CharField(("Role"), max_length=50, choices=[("ADMIN", "Admin"), ("SELLER", "Seller")], default='SELLER') 
    REQUIRED_FIELDS = []  
    objects = UserManager()

class Organization(models.Model):
    name = models.CharField(max_length=200, default="Atena")
    logo = models.ImageField(upload_to='company_logo/', null=True, blank=True)
    cnpj = models.CharField(max_length=20, blank=True, null=True, verbose_name="CNPJ")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    address = models.TextField(blank=True, null=True, verbose_name="Endereço")
    pix_key = models.CharField(max_length=100, blank=True, null=True, verbose_name="Chave PIX")
    receipt_footer_text = models.TextField(blank=True, null=True, verbose_name="Texto Rodapé Recibo")

    def save(self, *args, **kwargs):
        self.pk = 1
        super(Organization, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return self.name
