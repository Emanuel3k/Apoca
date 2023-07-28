from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.db import models

from pacientes.views import *
from pacientes.models import *
from .test_usuario import create_user


class ConsultasPerfilTestCase(TestCase):
    fixtures = [
        'testes/teste_cidades',
        'doencas',
        'medicamentos',
        'tipo_auxilios',
        'testes/teste_equipamentos',
        'testes/teste_pacientes',
        'testes/teste_entrega_auxilios.json'
    ]

    def setUp(self):
        self.factory = RequestFactory()
        self.user = create_user('Judit Polgar')

    def test_filtrar_auxilios(self):
        ''' filtrar_auxilios(request, pk)'''

        # Mocking a get request
        request = self.factory.get(reverse('pacientes:filtrar_auxilios', kwargs={'pk': 1}))
        request.user = self.user
        request.GET = request.GET.copy()

        # Teste 1
        request.GET['data_inicio'] = '01/11/2020'
        request.GET['data_fim'] = '30/11/2020'
        pk = 1
        response = filtrar_auxilios(request, pk)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), [
            {"nome": "Medicamento", "quantidade": 4},
            {"nome": "Empr\u00e9stimo de equipamento", "quantidade": 2},
            {"nome": "Cesta b\u00e1sica", "quantidade": 2},
            {"nome": "Suplemento alimentar", "quantidade": 1},
            {"nome": "Complemento alimentar", "quantidade": 0},
            {"nome": "Pr\u00f3tese feminina", "quantidade": 0},
            {"nome": "Item de convalescen\u00e7a", "quantidade": 0}
        ])

        # Teste 2
        request.GET['data_inicio'] = '19/11/2020'
        request.GET['data_fim'] = '30/11/2020'
        pk = 1
        response = filtrar_auxilios(request, pk)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), [
            {"nome": "Medicamento", "quantidade": 1},
            {"nome": "Empr\u00e9stimo de equipamento", "quantidade": 2},
            {"nome": "Cesta b\u00e1sica", "quantidade": 1},
            {"nome": "Suplemento alimentar", "quantidade": 0},
            {"nome": "Complemento alimentar", "quantidade": 0},
            {"nome": "Pr\u00f3tese feminina", "quantidade": 0},
            {"nome": "Item de convalescen\u00e7a", "quantidade": 0}
        ])

        # Teste 3 (usuario 2)
        request.GET['data_inicio'] = '01/11/2020'
        request.GET['data_fim'] = '30/11/2020'
        pk = 2
        response = filtrar_auxilios(request, pk)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), [
            {"nome": "Medicamento", "quantidade": 1},
            {"nome": "Empr\u00e9stimo de equipamento", "quantidade": 1},
            {"nome": "Cesta b\u00e1sica", "quantidade": 0},
            {"nome": "Suplemento alimentar", "quantidade": 0},
            {"nome": "Complemento alimentar", "quantidade": 0},
            {"nome": "Pr\u00f3tese feminina", "quantidade": 0},
            {"nome": "Item de convalescen\u00e7a", "quantidade": 0}
        ])

        # Teste 4 (variar pk e datas)
        request.GET['data_inicio'] = '13/10/2020'
        request.GET['data_fim'] = '30/10/2020'
        pk = 3
        response = filtrar_auxilios(request, pk)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), [
            {"nome": "Medicamento", "quantidade": 0},
            {"nome": "Empr\u00e9stimo de equipamento", "quantidade": 0},
            {"nome": "Cesta b\u00e1sica", "quantidade": 0},
            {"nome": "Suplemento alimentar", "quantidade": 0},
            {"nome": "Complemento alimentar", "quantidade": 0},
            {"nome": "Pr\u00f3tese feminina", "quantidade": 0},
            {"nome": "Item de convalescen\u00e7a", "quantidade": 0}
        ])

        # Teste 5
        request.GET['data_inicio'] = '15/10/2020'
        request.GET['data_fim'] = '30/10/2020'
        pk = 1
        response = filtrar_auxilios(request, pk)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), [
            {"nome": "Medicamento", "quantidade": 0},
            {"nome": "Empr\u00e9stimo de equipamento", "quantidade": 0},
            {"nome": "Cesta b\u00e1sica", "quantidade": 0},
            {"nome": "Suplemento alimentar", "quantidade": 1},
            {"nome": "Complemento alimentar", "quantidade": 0},
            {"nome": "Pr\u00f3tese feminina", "quantidade": 0},
            {"nome": "Item de convalescen\u00e7a", "quantidade": 0}
        ])

        # Teste 6
        request.GET['data_inicio'] = '01/10/2020'
        request.GET['data_fim'] = '01/11/2020'
        pk = 1
        response = filtrar_auxilios(request, pk)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), [
            {"nome": "Medicamento", "quantidade": 2},
            {"nome": "Empr\u00e9stimo de equipamento", "quantidade": 0},
            {"nome": "Cesta b\u00e1sica", "quantidade": 2},
            {"nome": "Suplemento alimentar", "quantidade": 1},
            {"nome": "Complemento alimentar", "quantidade": 0},
            {"nome": "Pr\u00f3tese feminina", "quantidade": 0},
            {"nome": "Item de convalescen\u00e7a", "quantidade": 0}
        ])

        # Teste 7
        request.GET['data_inicio'] = '01/09/2020'
        request.GET['data_fim'] = '01/12/2020'
        pk = 1
        response = filtrar_auxilios(request, pk)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), [
            {"nome": "Medicamento", "quantidade": 5},
            {"nome": "Empr\u00e9stimo de equipamento", "quantidade": 2},
            {"nome": "Cesta b\u00e1sica", "quantidade": 4},
            {"nome": "Suplemento alimentar", "quantidade": 2},
            {"nome": "Complemento alimentar", "quantidade": 1},
            {"nome": "Pr\u00f3tese feminina", "quantidade": 0},
            {"nome": "Item de convalescen\u00e7a", "quantidade": 0}
        ])

        # Teste 8 (criar tipos de auxilios e testar)
        tipo_auxilio_novo = TipoAuxilio.objects.create(nome='Meu auxílio', abreviacao='MA')
        request.GET['data_inicio'] = '01/09/2020'
        request.GET['data_fim'] = '01/12/2020'
        pk = 1
        response = filtrar_auxilios(request, pk)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), [
            {"nome": "Medicamento", "quantidade": 5},
            {"nome": "Empr\u00e9stimo de equipamento", "quantidade": 2},
            {"nome": "Cesta b\u00e1sica", "quantidade": 4},
            {"nome": "Suplemento alimentar", "quantidade": 2},
            {"nome": "Complemento alimentar", "quantidade": 1},
            {"nome": "Pr\u00f3tese feminina", "quantidade": 0},
            {"nome": "Item de convalescen\u00e7a", "quantidade": 0},
            {"nome": "Meu auxílio", "quantidade": 0}
        ])

        # Teste 9 (Novo auxilio entregue)
        Auxilio.objects.create(
            tipo=tipo_auxilio_novo,
            data_retirada='2020-09-02',
            hora_retirada='12:00',
            quantidade=2,
            paciente=Paciente.objects.get(pk=1)
        )
        request.GET['data_inicio'] = '01/09/2020'
        request.GET['data_fim'] = '01/12/2020'
        pk = 1
        response = filtrar_auxilios(request, pk)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), [
            {"nome": "Medicamento", "quantidade": 5},
            {"nome": "Empr\u00e9stimo de equipamento", "quantidade": 2},
            {"nome": "Cesta b\u00e1sica", "quantidade": 4},
            {"nome": "Suplemento alimentar", "quantidade": 2},
            {"nome": "Complemento alimentar", "quantidade": 1},
            {"nome": "Pr\u00f3tese feminina", "quantidade": 0},
            {"nome": "Item de convalescen\u00e7a", "quantidade": 0},
            {"nome": "Meu auxílio", "quantidade": 1}
        ])

        # Teste 10
        tipo_auxilio = TipoAuxilio.objects.get(pk=1)
        Auxilio.objects.create(
            tipo=tipo_auxilio,
            data_retirada='2020-10-02',
            hora_retirada='13:10',
            quantidade=3,
            paciente=Paciente.objects.get(pk=1)
        )
        request.GET['data_inicio'] = '01/09/2020'
        request.GET['data_fim'] = '01/12/2020'
        pk = 1
        response = filtrar_auxilios(request, pk)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), [
            {"nome": "Medicamento", "quantidade": 6},
            {"nome": "Empr\u00e9stimo de equipamento", "quantidade": 2},
            {"nome": "Cesta b\u00e1sica", "quantidade": 4},
            {"nome": "Suplemento alimentar", "quantidade": 2},
            {"nome": "Complemento alimentar", "quantidade": 1},
            {"nome": "Pr\u00f3tese feminina", "quantidade": 0},
            {"nome": "Item de convalescen\u00e7a", "quantidade": 0},
            {"nome": "Meu auxílio", "quantidade": 1}
        ])

        # Teste 11
        tipo_auxilo = TipoAuxilio.objects.get(pk=5)
        Auxilio.objects.create(
            tipo=tipo_auxilo,
            data_retirada='2020-06-15',
            hora_retirada='13:10',
            quantidade=1,
            paciente=Paciente.objects.get(pk=1)
        )
        request.GET['data_inicio'] = '01/06/2020'
        request.GET['data_fim'] = '01/07/2020'
        pk = 1
        response = filtrar_auxilios(request, pk)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), [
            {"nome": "Medicamento", "quantidade": 0},
            {"nome": "Empr\u00e9stimo de equipamento", "quantidade": 0},
            {"nome": "Cesta b\u00e1sica", "quantidade": 0},
            {"nome": "Suplemento alimentar", "quantidade": 0},
            {"nome": "Complemento alimentar", "quantidade": 1},
            {"nome": "Pr\u00f3tese feminina", "quantidade": 0},
            {"nome": "Item de convalescen\u00e7a", "quantidade": 0},
            {"nome": "Meu auxílio", "quantidade": 0}
        ])

        # Teste 12 (tentando deletar tipo de auxílio vinculado a auxílio)
        tipo_auxilio = TipoAuxilio.objects.get(pk=1)
        with self.assertRaises(models.ProtectedError):
            tipo_auxilio.delete()
        request.GET['data_inicio'] = '09/10/2020'
        request.GET['data_fim'] = '09/12/2020'
        pk = 1
        response = filtrar_auxilios(request, pk)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), [
            {"nome": "Medicamento", "quantidade": 4},
            {"nome": "Empr\u00e9stimo de equipamento", "quantidade": 2},
            {"nome": "Cesta b\u00e1sica", "quantidade": 2},
            {"nome": "Suplemento alimentar", "quantidade": 2},
            {"nome": "Complemento alimentar", "quantidade": 0},
            {"nome": "Pr\u00f3tese feminina", "quantidade": 0},
            {"nome": "Item de convalescen\u00e7a", "quantidade": 0},
            {"nome": "Meu auxílio", "quantidade": 0}
        ])

        # Teste 13 (criando novo tipo de auxílio)
        tipo_auxilio_novo = TipoAuxilio.objects.create(nome='Novo auxílio', abreviacao='NA')
        request.GET['data_inicio'] = '15/05/2020'
        request.GET['data_fim'] = '09/08/2020'
        pk = 5
        response = filtrar_auxilios(request, pk)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), [
            {"nome": "Medicamento", "quantidade": 0},
            {"nome": "Empr\u00e9stimo de equipamento", "quantidade": 0},
            {"nome": "Cesta b\u00e1sica", "quantidade": 0},
            {"nome": "Suplemento alimentar", "quantidade": 0},
            {"nome": "Complemento alimentar", "quantidade": 0},
            {"nome": "Pr\u00f3tese feminina", "quantidade": 0},
            {"nome": "Item de convalescen\u00e7a", "quantidade": 1},
            {"nome": "Meu auxílio", "quantidade": 0},
            {"nome": "Novo auxílio", "quantidade": 0}
        ])

        # Teste 14 (deletando um tipo de auxílio)
        tipo_auxilio = TipoAuxilio.objects.get(pk=9)
        tipo_auxilio.delete()
        request.GET['data_inicio'] = '15/05/2020'
        request.GET['data_fim'] = '09/08/2020'
        pk = 5
        response = filtrar_auxilios(request, pk)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), [
            {"nome": "Medicamento", "quantidade": 0},
            {"nome": "Empr\u00e9stimo de equipamento", "quantidade": 0},
            {"nome": "Cesta b\u00e1sica", "quantidade": 0},
            {"nome": "Suplemento alimentar", "quantidade": 0},
            {"nome": "Complemento alimentar", "quantidade": 0},
            {"nome": "Pr\u00f3tese feminina", "quantidade": 0},
            {"nome": "Item de convalescen\u00e7a", "quantidade": 1},
            {"nome": "Meu auxílio", "quantidade": 0}
        ])

        # Teste 15 (procurando um ano a frente)
        request.GET['data_inicio'] = '01/06/2021'
        request.GET['data_fim'] = '30/12/2021'
        pk = 1
        response = filtrar_auxilios(request, pk)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), [
            {"nome": "Medicamento", "quantidade": 0},
            {"nome": "Empr\u00e9stimo de equipamento", "quantidade": 0},
            {"nome": "Cesta b\u00e1sica", "quantidade": 0},
            {"nome": "Suplemento alimentar", "quantidade": 0},
            {"nome": "Complemento alimentar", "quantidade": 0},
            {"nome": "Pr\u00f3tese feminina", "quantidade": 0},
            {"nome": "Item de convalescen\u00e7a", "quantidade": 0},
            {"nome": "Meu auxílio", "quantidade": 0}
        ])

        # Teste 16
        request.GET['data_inicio'] = '01/06/2020'
        request.GET['data_fim'] = '30/12/2020'
        pk = 6
        response = filtrar_auxilios(request, pk)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), [
            {"nome": "Medicamento", "quantidade": 1},
            {"nome": "Empr\u00e9stimo de equipamento", "quantidade": 0},
            {"nome": "Cesta b\u00e1sica", "quantidade": 0},
            {"nome": "Suplemento alimentar", "quantidade": 0},
            {"nome": "Complemento alimentar", "quantidade": 0},
            {"nome": "Pr\u00f3tese feminina", "quantidade": 1},
            {"nome": "Item de convalescen\u00e7a", "quantidade": 0},
            {"nome": "Meu auxílio", "quantidade": 0}
        ])

        # Teste 17 (criando nova entrega de auxílio)
        Auxilio.objects.create(
            tipo=TipoAuxilio.objects.get(pk=3),
            data_retirada='2020-09-03',
            hora_retirada='12:00',
            quantidade=2,
            paciente=Paciente.objects.get(pk=6)
        )
        request.GET['data_inicio'] = '01/06/2020'
        request.GET['data_fim'] = '30/12/2020'
        pk = 6
        response = filtrar_auxilios(request, pk)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), [
            {"nome": "Medicamento", "quantidade": 1},
            {"nome": "Empr\u00e9stimo de equipamento", "quantidade": 0},
            {"nome": "Cesta b\u00e1sica", "quantidade": 1},
            {"nome": "Suplemento alimentar", "quantidade": 0},
            {"nome": "Complemento alimentar", "quantidade": 0},
            {"nome": "Pr\u00f3tese feminina", "quantidade": 1},
            {"nome": "Item de convalescen\u00e7a", "quantidade": 0},
            {"nome": "Meu auxílio", "quantidade": 0}
        ])

        # Teste 18
        request.GET['data_inicio'] = '05/10/2020'
        request.GET['data_fim'] = '29/11/2020'
        pk = 7
        response = filtrar_auxilios(request, pk)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), [
            {"nome": "Medicamento", "quantidade": 1},
            {"nome": "Empr\u00e9stimo de equipamento", "quantidade": 1},
            {"nome": "Cesta b\u00e1sica", "quantidade": 0},
            {"nome": "Suplemento alimentar", "quantidade": 0},
            {"nome": "Complemento alimentar", "quantidade": 0},
            {"nome": "Pr\u00f3tese feminina", "quantidade": 0},
            {"nome": "Item de convalescen\u00e7a", "quantidade": 0},
            {"nome": "Meu auxílio", "quantidade": 0}
        ])

        # Teste 19
        request.GET['data_inicio'] = '17/07/2020'
        request.GET['data_fim'] = '30/11/2020'
        pk = 7
        response = filtrar_auxilios(request, pk)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), [
            {"nome": "Medicamento", "quantidade": 2},
            {"nome": "Empr\u00e9stimo de equipamento", "quantidade": 1},
            {"nome": "Cesta b\u00e1sica", "quantidade": 0},
            {"nome": "Suplemento alimentar", "quantidade": 0},
            {"nome": "Complemento alimentar", "quantidade": 1},
            {"nome": "Pr\u00f3tese feminina", "quantidade": 0},
            {"nome": "Item de convalescen\u00e7a", "quantidade": 1},
            {"nome": "Meu auxílio", "quantidade": 0}
        ])

        # Teste 20
        request.GET['data_inicio'] = '02/08/2020'
        request.GET['data_fim'] = '30/09/2020'
        pk = 9
        response = filtrar_auxilios(request, pk)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), [
            {"nome": "Medicamento", "quantidade": 1},
            {"nome": "Empr\u00e9stimo de equipamento", "quantidade": 0},
            {"nome": "Cesta b\u00e1sica", "quantidade": 0},
            {"nome": "Suplemento alimentar", "quantidade": 0},
            {"nome": "Complemento alimentar", "quantidade": 1},
            {"nome": "Pr\u00f3tese feminina", "quantidade": 0},
            {"nome": "Item de convalescen\u00e7a", "quantidade": 0},
            {"nome": "Meu auxílio", "quantidade": 0}
        ])