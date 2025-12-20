from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .manage import UserManager
from django.core.validators import RegexValidator


phone_regex = RegexValidator(
    regex=r'^\+?\d{9,15}$',
    message="Le numéro doit être au format international. Ex: +221771234567"
)

class User(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = [
        ('user', 'Utilisateur'),
        ('admin', 'Admin'),
    ]
    LEVEL_CHOICES = [
        ("beginner", "Débutant"),
        ("advanced", "Avancé"),
    ]

    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        null=True,
        blank=True
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
    first_name = models.CharField(max_length=100, db_index=True)
    last_name = models.CharField(max_length=100, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )
    GENDER_CHOICES = [('masculin', 'Masculin'), ('feminin', 'Feminin')]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='masculin')
    address = models.CharField(max_length=255, blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        unique=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    objects = UserManager()


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['id']