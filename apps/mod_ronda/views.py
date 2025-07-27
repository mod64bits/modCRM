import io

import qrcode
from PIL import ImageFont, Image, ImageDraw
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import  RondaPoint, RondaLog
from .serializers import RondaPointSerializer, RondaLogSerializer
from apps.base.permissions import IsAdmin, IsSindicoOrAdmin, IsManagerRole, CanManageRondaPoints


class RondaPointViewSet(viewsets.ModelViewSet):

    serializer_class = RondaPointSerializer

    def get_permissions(self):

        """Define permissões por ação (ATUALIZADO)."""
        # Ações de escrita e geração de QR Code agora usam CanManageRondaPoints
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'generate_qrcode']:
            self.permission_classes = [CanManageRondaPoints]
        else: # list, retrieve
            self.permission_classes = [IsManagerRole]
        return super().get_permissions()

    def get_queryset(self):
        """Filtra pontos de ronda pela empresa do usuário logado."""
        return RondaPoint.objects.filter(company=self.request.user.company)

    def perform_create(self, serializer):
        """Associa o novo ponto de ronda à empresa do usuário."""
        serializer.save(company=self.request.user.company)

    # ATUALIZADO: Endpoint agora gera e retorna uma imagem PNG
    @action(detail=True, methods=['get'], url_path='generate-qrcode')
    def generate_qrcode(self, request, pk=None):
        """
        Gera uma imagem PNG do QR Code contendo o nome e a localização do ponto.
        O QR Code em si contém o UUID para leitura pelo app.
        """
        ronda_point = self.get_object()

         # 1. Dados a serem codificados no QR Code (robusto para o app)
        qr_code_data = f"RONDA_API::{ronda_point.id}"

        # 2. Gerar a imagem do QR Code
        qr_img = qrcode.make(qr_code_data, box_size=10, border=4)

                # 3. Preparar para adicionar texto (Nome e Descrição)
        qr_width, qr_height = qr_img.size
        padding = 20
        text_area_height = 80 # Espaço extra para o texto abaixo

        # Tente carregar uma fonte, use a padrão como fallback
        try:
            # Para ambientes de produção, especifique o caminho completo da fonte
            # Ex: '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
            title_font = ImageFont.truetype("arial.ttf", 24)
            desc_font = ImageFont.truetype("arial.ttf", 16)
        except IOError:
            title_font = ImageFont.load_default()
            desc_font = ImageFont.load_default()

        # 4. Criar a imagem final (fundo branco)
        final_width = qr_width + (2 * padding)
        final_height = qr_height + text_area_height + (2 * padding)
        final_img = Image.new('RGB', (final_width, final_height), 'white')
        draw = ImageDraw.Draw(final_img)

        # 5. Colar a imagem do QR Code na imagem final
        final_img.paste(qr_img, (padding, padding))

        # 6. Adicionar o texto
        text_y_start = qr_height + (2 * padding)
        # Nome do Ponto
        draw.text((padding, text_y_start), ronda_point.name, font=title_font, fill="black")
        # Descrição da Localização
        draw.text((padding, text_y_start + 30), ronda_point.location_description, font=desc_font, fill="black")

        # 7. Salvar a imagem final em um buffer de memória
        buffer = io.BytesIO()
        final_img.save(buffer, format='PNG')
        buffer.seek(0)

        # 8. Retornar a imagem na resposta HTTP
        return HttpResponse(buffer, content_type='image/png')



class RondaLogViewSet(viewsets.ModelViewSet):
    serializer_class = RondaLogSerializer
    http_method_names = ['get', 'post', 'head', 'options'] # Apenas permite criar e visualizar
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'timestamp': ['gte', 'lte', 'date']}  # Permite filtrar por: >=, <=, e data exata

    def get_permissions(self):
        """
        - Qualquer usuário autenticado pode criar um log (fazer uma ronda).
        - Apenas cargos de gerência podem listar/ver os relatórios.
        """
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsManagerRole]
        return super().get_permissions()

    def get_queryset(self):
        """Filtra logs pela empresa do usuário logado."""
        return RondaLog.objects.filter(user__company=self.request.user.company)

    def perform_create(self, serializer):
        """
        Associa o log ao usuário que está fazendo a requisição (o vigilante).
        Valida se o ponto de ronda pertence à mesma empresa do usuário.
        """
        ronda_point_id = serializer.validated_data['ronda_point'].id
        ronda_point = RondaPoint.objects.get(id=ronda_point_id)

        if ronda_point.company != self.request.user.company:
            raise serializers.ValidationError("Este ponto de ronda não pertence à sua empresa.")

        serializer.save(user=self.request.user)