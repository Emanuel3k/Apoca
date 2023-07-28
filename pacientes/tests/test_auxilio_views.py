from django.test import TestCase, RequestFactory
from django.urls import reverse

from pacientes.models import Auxilio
from pacientes.views.auxilios import *
from .test_usuario import create_user

class AuxilioTestCase(TestCase):
    """ attrs: [...] """
    fixtures = [
        'tipo_auxilios',
        'medicamentos',
        'testes/teste_equipamentos'
    ]

    def setUp(self):
        self.factory = RequestFactory()
        self.user = create_user('Judit Polgar')

    def test_listar_auxilios(self):
        # Criando uma request GET falsa
        request = self.factory.get(reverse('pacientes:listar_auxilios'))
        request.user = self.user
        request.GET = request.GET.copy()
        response = listar_auxilios(request)

        self.assertIs(response.status_code, 200)