from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        SINDICO = "SINDICO", "Síndico"
        GERENTE = "GERENTE", "Gerente"
        VIGILANTE = "VIGILANTE", "Vigilante"

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.VIGILANTE)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, null=True, blank=True, related_name="employees")

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        # O related_name resolve o conflito
        related_name="account_user_groups",
        related_query_name="user",
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        # O related_name resolve o conflito
        related_name="account_user_permissions",
        related_query_name="user",
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)
