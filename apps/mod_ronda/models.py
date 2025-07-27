import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class RondaPoint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Nome do Ponto")
    location_description = models.TextField(verbose_name="Descrição da Localização")
    company = models.ForeignKey("company.Company", on_delete=models.CASCADE, related_name="ronda_points")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.company.name})"

class RondaLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ronda_point = models.ForeignKey(RondaPoint, on_delete=models.PROTECT, related_name="logs")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="ronda_logs")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Data e Hora")

    def __str__(self):
        return f"Ronda em {self.ronda_point.name} por {self.user.username} em {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']