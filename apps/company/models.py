from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Nome da Empresa/Condomínio")

    def __str__(self):
        return self.name
