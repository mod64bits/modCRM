from rest_framework import viewsets
from .models import User
from apps.base.permissions import IsAdmin
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    # Apenas Admins podem acessar este endpoint
    permission_classes = [IsAdmin]

    def get_queryset(self):
        # Admin vê apenas usuários de sua própria empresa
        return User.objects.filter(company=self.request.user.company)

    def perform_create(self, serializer):
        # Associa o novo usuário à mesma empresa do Admin que o está criando
        serializer.save(company=self.request.user.company)

