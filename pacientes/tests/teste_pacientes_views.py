from django.test import TestCase, Client

from pacientes.models import *
from pacientes.views.utilitarios import *


class PacienteTestCase(TestCase):
    """ attrs: [...] """
    fixtures = [
        'testes/teste_cidades',
        'doencas',
        'testes/teste_pacientes'
    ]

    def setUp(self):
        pass

    def test_validators_cpf(self):
        cpf1 = '063.234.543-32'
        cpf2 = '06323454332'
        self.assertEqual(formatar_cpf(cpf2), cpf1)
        self.assertEqual(desformatar_cpf(cpf1), cpf2)
        cpf1 = '746.234.897-45'
        cpf2 = '74623489745'
        self.assertEqual(formatar_cpf(cpf2), cpf1)
        self.assertEqual(desformatar_cpf(cpf1), cpf2)

    def test_cadastrar_telefone(self):
        p1 = Paciente.objects.get(pk=1)
        ddd = '21'
        telefone = '999999999'
        cadastrar_telefone(ddd, telefone, p1)
        tel = Telefone.objects.get(paciente=p1)
        self.assertEqual(tel.ddd, ddd)
        self.assertEqual(tel.telefone, telefone)
        self.assertEqual(p1.pk, tel.paciente.pk)
        self.assertIs(Telefone.objects.all().count(), 1)

        cadastrar_telefone('21', '', p1)
        cadastrar_telefone('  ', '', p1)
        cadastrar_telefone('47', '  ', p1)
        cadastrar_telefone('', '435353', p1)
        self.assertIs(Telefone.objects.all().count(), 1)

    def test_cadastrar_responsavel(self):
        p1 = Paciente.objects.get(pk=2)
        responsavel = 'Nefertiti'
        cadastrar_responsavel(responsavel, p1)
        nefer = Responsavel.objects.get(paciente=p1)
        self.assertEqual(nefer.nome, responsavel)
        self.assertEqual(p1.pk, nefer.paciente.pk)
        self.assertIs(Responsavel.objects.all().count(), 1)

        cadastrar_responsavel(' ', p1)
        cadastrar_responsavel('', p1)
        self.assertIs(Responsavel.objects.all().count(), 1)
