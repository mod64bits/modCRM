from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'


class IsSindico(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'SINDICO'


class IsGerente(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'GERENTE'


# Permissão para Síndico ou Admin
class IsSindicoOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'SINDICO' or request.user.role == 'ADMIN')




class CanManageRondaPoints(BasePermission):
    """
    Permite acesso a usuários com papéis de gestão (Admin, Síndico, Gerente).
    """
    message = "Apenas Admin, Síndico ou Gerente podem realizar esta ação."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['ADMIN', 'SINDICO', 'GERENTE']

# Permissão para qualquer cargo de gestão (ver relatórios)
class IsManagerRole(BasePermission):
     def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['ADMIN', 'SINDICO', 'GERENTE']