from rest_framework import viewsets
from .models import Company
from .serializers import CompanySerializer
from apps.base.permissions import IsAdmin


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdmin] # Apenas Admins do sistema podem ver e gerenciar empresas

