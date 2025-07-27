from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.account.models import User
from apps.company.models import Company
from apps.mod_ronda.models import RondaPoint


class RondaAPITestCase(APITestCase):


    def setUp(self):
        # Criar empresas
        self.company_a = Company.objects.create(name="Condomínio A")
        self.company_b = Company.objects.create(name="Condomínio B")

        # Criar usuários com diferentes papéis na Empresa A
        self.admin_a = User.objects.create_user(username="admin_a", password="password", company=self.company_a, role=User.Role.ADMIN)
        self.sindico_a = User.objects.create_user(username="sindico_a", password="password", company=self.company_a, role=User.Role.SINDICO)
        self.gerente_a = User.objects.create_user(username="gerente_a", password="password", company=self.company_a, role=User.Role.GERENTE)
        self.vigilante_a = User.objects.create_user(username="vigilante_a", password="password", company=self.company_a, role=User.Role.VIGILANTE)

        # Criar usuário na Empresa B
        self.sindico_b = User.objects.create_user(username="sindico_b", password="password", company=self.company_b, role=User.Role.SINDICO)

        # Criar um ponto de ronda na Empresa A
        self.point_a = RondaPoint.objects.create(name="Garagem G1", location_description="Portão principal da garagem", company=self.company_a)

    def test_sindico_can_create_ronda_point(self):
        """Verifica se o Síndico pode criar um ponto de ronda."""
        self.client.force_authenticate(user=self.sindico_a)
        url = reverse('rondapoint-list')
        data = {'name': 'Piscina', 'location_description': 'Área de lazer da piscina'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RondaPoint.objects.count(), 2)

    def test_gerente_cannot_create_ronda_point(self):
        """Verifica se o Gerente NÃO pode criar um ponto de ronda."""
        self.client.force_authenticate(user=self.gerente_a)
        url = reverse('rondapoint-list')
        data = {'name': 'Salão de Festas', 'location_description': 'Entrada principal'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_vigilante_can_create_ronda_log(self):
        """Verifica se um Vigilante pode registrar uma ronda."""
        self.client.force_authenticate(user=self.vigilante_a)
        url = reverse('rondalog-list')
        data = {'ronda_point': self.point_a.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user_name'], self.vigilante_a.get_full_name())

    def test_user_cannot_see_data_from_another_company(self):
        """Verifica o isolamento de dados entre empresas."""
        # sindico_b (da empresa B) tenta ver os pontos da empresa A
        self.client.force_authenticate(user=self.sindico_b)
        url = reverse('rondapoint-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # A resposta deve estar vazia, pois não há pontos na empresa B
        self.assertEqual(len(response.data), 0)

    def test_sindico_can_generate_qrcode_data(self):



        """Verifica se o Síndico pode acessar a rota para gerar dados do QR Code."""
        self.client.force_authenticate(user=self.sindico_a)
        url = reverse('rondapoint-generate-qrcode', kwargs={'pk': self.point_a.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('qr_code_data', response.data)
        self.assertEqual(response.data['qr_code_data'], f"RONDA_API::{self.point_a.id}")

    def test_gerente_CAN_create_ronda_point_now(self):

        """Verifica se o Gerente AGORA PODE criar um ponto de ronda."""
        self.client.force_authenticate(user=self.gerente_a)
        url = reverse('rondapoint-list')
        data = {'name': 'Salão de Festas', 'location_description': 'Entrada principal'}
        response = self.client.post(url, data)
        # A permissão foi alterada, então agora esperamos 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RondaPoint.objects.last().name, 'Salão de Festas')

    def test_vigilante_cannot_create_ronda_point(self):
        """Verifica se o Vigilante AINDA NÃO PODE criar um ponto de ronda."""
        self.client.force_authenticate(user=self.vigilante_a)
        url = reverse('rondapoint-list')
        data = {'name': 'Bicicletário', 'location_description': 'Subsolo'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_generate_qrcode_returns_image(self):
        """Verifica se a rota de QR Code retorna uma imagem PNG."""
        self.client.force_authenticate(user=self.sindico_a)
        url = reverse('rondapoint-generate-qrcode', kwargs={'pk': self.point_a.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verifica o tipo de conteúdo da resposta
        self.assertEqual(response['Content-Type'], 'image/png')
