from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from apps.company.models import Company
from apps.mod_ronda.models import RondaPoint, RondaLog


class CustomUserAdmin(UserAdmin):
    # Campos a serem exibidos na lista de usuários
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'company', 'is_staff')

    # Adiciona 'role' e 'company' aos filtros da barra lateral
    list_filter = ('role', 'company', 'is_staff', 'is_superuser', 'groups')


    fieldsets = UserAdmin.fieldsets + (
        ('Controle de Acesso da Empresa', {'fields': ('role', 'company')}),
    )
    # Elas informam ao formulário de CRIAÇÃO sobre os novos campos.
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Controle de Acesso da Empresa', {'fields': ('role', 'company')}),
    )


# Registra os modelos no admin
admin.site.register(User, CustomUserAdmin)
admin.site.register(Company)
admin.site.register(RondaPoint)
admin.site.register(RondaLog)