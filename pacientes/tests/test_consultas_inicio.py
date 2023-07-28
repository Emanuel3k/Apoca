from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.db import models
from django.utils import timezone

# from datetime import datetime
from dateutil.relativedelta import relativedelta
import random
import json

from pacientes.views import *
from pacientes.models import *
from .test_usuario import create_user


class ConsultasInicioTestCase(TestCase):
    fixtures = [
        'testes/teste_cidades',
        'doencas',
        'medicamentos',
        'tipo_auxilios',
        'tipo_consulta.json',
        'testes/teste_equipamentos',
        'testes/teste_pacientes',
        'testes/teste_entrega_auxilios.json',
        'testes/teste_consulta.json',
    ]

    def setUp(self):
        self.factory = RequestFactory()
        self.user = create_user('Judit Polgar')

    def test_consulta_atividades_diarias(self):
        atv_diaria = consulta_atividades_diarias()
        # inicialmente nao ha nenhuma atividade
        self.assertIs(atv_diaria['pacientes'], 0)
        self.assertIs(atv_diaria['auxilios'], 0)
        self.assertIs(atv_diaria['consultas'], 0)
        self.assertIs(atv_diaria['exames'], 0)

        # Cadastro de Paciente
        paciente = {
            'nome': 'Jaum',
            'sexo': 'Masculino',
            'data_nascimento': timezone.localdate() - relativedelta(years=random.randint(20, 69)),
            'cpf': str(random.randint(222222, 9999999)),
            'rg': str(random.randint(111111, 9999999)),
            'cartao_sus': str(random.randint(111111, 9999999)),
            'nome_mae': random.choice(['Ana','Maria', 'Antônia']),
            'conjuge': random.choice(['Darcy','Paulinho', 'Jonas', 'Tião']),
            'profissao': random.choice(['Fazendeira','Padeira', 'Médica']),
            'outros_casos': random.choice([True, False]),
            'composicao_familiar': random.randint(1, 10),
            'renda_familiar': random.randint(900, 99999),
            'doenca': random.choice(['Tumores Pituitários', 'Tumores Ósseos',
            'Tumores Neuroendócrinos', 'Tumores Cerebrais/SNC em crinaças']),
            'metastase': random.choice([True, False]),
            'diabetes': random.choice([True, False]),
            'referencia': random.choice(['Esquina do bar', 'Casa azul', 'Pracinha']),
            'logradouro': random.choice(['Casa', 'Ap']),
            'numero': random.randint(90, 9999),
            'bairro': random.choice(['Campo da água azul', 'Centro', 'Capão redondo']),
            'cidade': random.choice(['Canoinhas', 'Três Barras', 'Curitiba']),
            'complemento': random.choice(['Fundos', 'Ap 33', 'B']),
            'raca': 'Não informado'
        }
        paciente1 = self.criar_paciente(paciente)
        # Exame de teste
        Exame.objects.create(
            tipo = "Covid - 19",
            data = timezone.now(),
            paciente = paciente1
        )
        # Entrega de auxílios de teste
        Auxilio.objects.create(
            tipo = TipoAuxilio.objects.get(pk=1),
            quantidade = 10,
            data_retirada = timezone.now(),
            hora_retirada = '10:15:00',
            medicamento = Medicamento.objects.get(pk=1),
            paciente = Paciente.objects.get(pk=1)
        )

        Auxilio.objects.create(
            tipo = TipoAuxilio.objects.get(pk=3),
            quantidade = 1,
            data_retirada = timezone.now(),
            hora_retirada = '11:25:00',
            paciente = paciente1
        )
        # Consultas de teste
        Consulta.objects.create(
            tipo = TipoConsulta.objects.get(pk=1),
            data = timezone.now(),
            exames = 'Tumografia',
            paciente = paciente1
        )

        Consulta.objects.create(
            tipo = TipoConsulta.objects.get(pk=2),
            data = timezone.now(),
            paciente = Paciente.objects.get(pk=3)
        )

        Consulta.objects.create(
            tipo = TipoConsulta.objects.get(pk=1),
            data = timezone.now(),
            exames = 'Raio-X',
            paciente = Paciente.objects.get(pk=4)
        )

        # Teste 2
        atv_diaria = consulta_atividades_diarias()
        self.assertIs(atv_diaria['pacientes'], 1)
        self.assertIs(atv_diaria['exames'], 1)
        self.assertIs(atv_diaria['auxilios'], 2)
        self.assertIs(atv_diaria['consultas'], 3)

        paciente = {
            'nome': 'Mariana',
            'sexo': 'Feminino',
            'data_nascimento': timezone.localdate() - relativedelta(years=random.randint(20, 69)),
            'cpf': str(random.randint(222222, 9999999)),
            'rg': str(random.randint(111111, 9999999)),
            'cartao_sus': str(random.randint(111111, 9999999)),
            'nome_mae': random.choice(['Ana','Maria', 'Antônia']),
            'composicao_familiar': random.randint(1, 10),
            'renda_familiar': random.randint(900, 99999),
            'doenca': random.choice(['Tumores Pituitários', 'Tumores Ósseos',
            'Tumores Neuroendócrinos', 'Tumores Cerebrais/SNC em crinaças']),
            'referencia': random.choice(['Esquina do bar', 'Casa azul', 'Pracinha']),
            'logradouro': random.choice(['Casa', 'Ap']),
            'numero': random.randint(90, 9999),
            'bairro': random.choice(['Campo da água azul', 'Centro', 'Capão redondo']),
            'cidade': random.choice(['Canoinhas', 'Três Barras', 'Curitiba']),
            'raca': 'Preta'
        }
        paciente3 = self.criar_paciente(paciente)
        # Exame de teste
        Exame.objects.create(
            tipo="Raio-X",
            data=timezone.now(),
            paciente = paciente3
        )
        # Consultas de teste
        Consulta.objects.create(
            tipo = TipoConsulta.objects.get(pk=3),
            data = timezone.now(),
            paciente = Paciente.objects.get(pk=7)
        )

        # Teste 3
        atv_diaria = consulta_atividades_diarias()
        self.assertIs(atv_diaria['pacientes'], 2)
        self.assertIs(atv_diaria['exames'], 2)
        self.assertIs(atv_diaria['auxilios'], 2)
        self.assertIs(atv_diaria['consultas'], 4)

        # Exame de teste
        Exame.objects.create(
            tipo = "Radiografia",
            data = timezone.now(),
            paciente = Paciente.objects.get(pk=5)
        )

        Exame.objects.create(
            tipo = "Mamografia",
            data = timezone.now(),
            paciente = Paciente.objects.get(pk=8)
        )
        # Entrega de auxílio de teste
        Auxilio.objects.create(
            tipo = TipoAuxilio.objects.get(pk=2),
            quantidade = 2,
            data_retirada = timezone.now(),
            hora_retirada = '14:00:00',
            equipamento = Equipamento.objects.get(pk=4),
            paciente = paciente3
        )

        Auxilio.objects.create(
            tipo = TipoAuxilio.objects.get(pk=4),
            quantidade = 5,
            data_retirada = timezone.now(),
            hora_retirada = '14:40:20',
            paciente = Paciente.objects.get(pk=9)
        )
        # Consultas de teste
        Consulta.objects.create(
            tipo = TipoConsulta.objects.get(pk=2),
            data = timezone.now(),
            paciente = Paciente.objects.get(pk=4)
        )

        # Teste 4
        atv_diaria = consulta_atividades_diarias()
        self.assertIs(atv_diaria['pacientes'], 2)
        self.assertIs(atv_diaria['exames'], 4)
        self.assertIs(atv_diaria['auxilios'], 4)
        self.assertIs(atv_diaria['consultas'], 5)

        paciente = {
            'nome': 'Luiz',
            'sexo': 'Masculino',
            'data_nascimento': timezone.localdate() - relativedelta(years=random.randint(20, 69)),
            'cpf': str(random.randint(222222, 9999999)),
            'rg': str(random.randint(111111, 9999999)),
            'cartao_sus': str(random.randint(111111, 9999999)),
            'nome_mae': random.choice(['Ana','Maria', 'Antônia']),
            'composicao_familiar': random.randint(1, 10),
            'renda_familiar': random.randint(900, 99999),
            'doenca': random.choice(['Tumores Pituitários', 'Tumores Ósseos',
            'Tumores Neuroendócrinos', 'Tumores Cerebrais/SNC em crinaças']),
            'referencia': random.choice(['Esquina do bar', 'Casa azul', 'Pracinha']),
            'logradouro': random.choice(['Casa', 'Ap']),
            'numero': random.randint(90, 9999),
            'bairro': random.choice(['Campo da água azul', 'Centro', 'Capão redondo']),
            'cidade': random.choice(['Canoinhas', 'Três Barras', 'Curitiba']),
            'raca': 'Amarela'
        }
        paciente4 = self.criar_paciente(paciente)

        paciente = {
            'nome': 'Marcelo',
            'sexo': 'Masculino',
            'data_nascimento': timezone.localdate() - relativedelta(years=random.randint(20, 69)),
            'cpf': str(random.randint(222222, 9999999)),
            'rg': str(random.randint(111111, 9999999)),
            'cartao_sus': str(random.randint(111111, 9999999)),
            'nome_mae': random.choice(['Ana','Maria', 'Antônia']),
            'composicao_familiar': random.randint(1, 10),
            'renda_familiar': random.randint(900, 99999),
            'doenca': random.choice(['Tumores Pituitários', 'Tumores Ósseos',
            'Tumores Neuroendócrinos', 'Tumores Cerebrais/SNC em crinaças']),
            'referencia': random.choice(['Esquina do bar', 'Casa azul', 'Pracinha']),
            'logradouro': random.choice(['Casa', 'Ap']),
            'numero': random.randint(90, 9999),
            'bairro': random.choice(['Campo da água azul', 'Centro', 'Capão redondo']),
            'cidade': random.choice(['Canoinhas', 'Três Barras', 'Curitiba']),
            'raca': 'Branca'
        }
        paciente5 = self.criar_paciente(paciente)

        # Exames de teste
        Exame.objects.create(
            tipo = "Ecodopler",
            data = timezone.now(),
            paciente = paciente5
        )

        # Teste 5
        atv_diaria = consulta_atividades_diarias()
        self.assertIs(atv_diaria['pacientes'], 4)
        self.assertIs(atv_diaria['exames'], 5)
        self.assertIs(atv_diaria['auxilios'], 4)
        self.assertIs(atv_diaria['consultas'], 5)

        paciente = {
            'nome': 'Julia',
            'sexo': 'Feminino',
            'data_nascimento': timezone.localdate() - relativedelta(years=random.randint(20, 69)),
            'cpf': str(random.randint(222222, 9999999)),
            'rg': str(random.randint(111111, 9999999)),
            'cartao_sus': str(random.randint(111111, 9999999)),
            'nome_mae': random.choice(['Ana','Maria', 'Antônia']),
            'composicao_familiar': random.randint(1, 10),
            'renda_familiar': random.randint(900, 99999),
            'doenca': random.choice(['Tumores Pituitários', 'Tumores Ósseos',
            'Tumores Neuroendócrinos', 'Tumores Cerebrais/SNC em crinaças']),
            'referencia': random.choice(['Esquina do bar', 'Casa azul', 'Pracinha']),
            'logradouro': random.choice(['Casa', 'Ap']),
            'numero': random.randint(90, 9999),
            'bairro': random.choice(['Campo da água azul', 'Centro', 'Capão redondo']),
            'cidade': random.choice(['Canoinhas', 'Três Barras', 'Curitiba']),
            'raca': 'Amarela'
        }
        paciente6 = self.criar_paciente(paciente)

        paciente = {
            'nome': 'Paulo',
            'sexo': 'Masculino',
            'data_nascimento': timezone.localdate() - relativedelta(years=random.randint(20, 69)),
            'cpf': str(random.randint(222222, 9999999)),
            'rg': str(random.randint(111111, 9999999)),
            'cartao_sus': str(random.randint(111111, 9999999)),
            'nome_mae': random.choice(['Ana','Maria', 'Antônia']),
            'composicao_familiar': random.randint(1, 10),
            'renda_familiar': random.randint(900, 99999),
            'doenca': random.choice(['Tumores Pituitários', 'Tumores Ósseos',
            'Tumores Neuroendócrinos', 'Tumores Cerebrais/SNC em crinaças']),
            'referencia': random.choice(['Esquina do bar', 'Casa azul', 'Pracinha']),
            'logradouro': random.choice(['Casa', 'Ap']),
            'numero': random.randint(90, 9999),
            'bairro': random.choice(['Campo da água azul', 'Centro', 'Capão redondo']),
            'cidade': random.choice(['Canoinhas', 'Três Barras', 'Curitiba']),
            'raca': 'Branca'
        }
        paciente7 = self.criar_paciente(paciente)

        # Exames de teste
        Exame.objects.create(
            tipo = "Ecodopler",
            data = timezone.now(),
            paciente = paciente5
        )
        # Entrega de auxílio de teste
        Auxilio.objects.create(
            tipo = TipoAuxilio.objects.get(pk=6),
            quantidade = 1,
            data_retirada = timezone.now(),
            hora_retirada = '16:20:00',
            paciente = Paciente.objects.get(pk=10)
        )

        Auxilio.objects.create(
            tipo = TipoAuxilio.objects.get(pk=1),
            quantidade = 3,
            data_retirada = timezone.now(),
            hora_retirada = '16:50:55',
            medicamento = Medicamento.objects.get(pk=3),
            paciente = Paciente.objects.get(pk=6)
        )
        # Consultas de teste
        Consulta.objects.create(
            tipo = TipoConsulta.objects.get(pk=3),
            data = timezone.now(),
            paciente = paciente6
        )

        # Teste 6
        atv_diaria = consulta_atividades_diarias()
        self.assertIs(atv_diaria['pacientes'], 6)
        self.assertIs(atv_diaria['exames'], 6)
        self.assertIs(atv_diaria['auxilios'], 6)
        self.assertIs(atv_diaria['consultas'], 6)

        # Criando atividades com a data diferente da atual
        # Exame realizado no dia anterior do atual
        Exame.objects.create(
            tipo = "Raio-X",
            data = timezone.localdate() - relativedelta(days=1),
            paciente = paciente5
        )

        # Consulta realizada no dia seguinte do atual
        Consulta.objects.create(
            tipo = TipoConsulta.objects.get(pk=2),
            data = timezone.localdate() + relativedelta(days=1),
            paciente = Paciente.objects.get(pk=1)
        )

        # Teste 7, não deve mudar nada pois a data das atividades é diferente da atual
        atv_diaria = consulta_atividades_diarias()
        self.assertIs(atv_diaria['pacientes'], 6)
        self.assertIs(atv_diaria['exames'], 6)
        self.assertIs(atv_diaria['auxilios'], 6)
        self.assertIs(atv_diaria['consultas'], 6)


    def test_consulta_racas(self):
        racas = consulta_racas()
        # Teste 1 - fixtures
        self.assertIs(racas[0], 5)
        self.assertIs(racas[1], 1)
        self.assertIs(racas[2], 2)
        self.assertIs(racas[3], 1)
        self.assertIs(racas[4], 0)
        self.assertIs(racas[5], 0)

        # Teste 2 - adicionando um paciente
        # Cadastro de Paciente
        paciente = {
            'nome': 'Jaum',
            'sexo': 'Masculino',
            'data_nascimento': timezone.localdate() - relativedelta(years=random.randint(20, 69)),
            'cpf': str(random.randint(222222, 9999999)),
            'rg': str(random.randint(111111, 9999999)),
            'cartao_sus': str(random.randint(111111, 9999999)),
            'nome_mae': random.choice(['Ana','Maria', 'Antônia']),
            'composicao_familiar': random.randint(1, 10),
            'renda_familiar': random.randint(900, 99999),
            'doenca': random.choice(['Tumores Pituitários', 'Tumores Ósseos',
            'Tumores Neuroendócrinos', 'Tumores Cerebrais/SNC em crinaças']),
            'referencia': random.choice(['Esquina do bar', 'Casa azul', 'Pracinha']),
            'logradouro': random.choice(['Casa', 'Ap']),
            'numero': random.randint(90, 9999),
            'bairro': random.choice(['Campo da água azul', 'Centro', 'Capão redondo']),
            'cidade': random.choice(['Canoinhas', 'Três Barras', 'Curitiba']),
            'raca': 'Indígena'
        }
        paciente2 = self.criar_paciente(paciente)

        racas = consulta_racas()
        self.assertIs(racas[0], 5)
        self.assertIs(racas[1], 1)
        self.assertIs(racas[2], 2)
        self.assertIs(racas[3], 1)
        self.assertIs(racas[4], 1)
        self.assertIs(racas[5], 0)

        # Teste 3
        paciente = {
            'nome': 'Milena',
            'sexo': 'Feminino',
            'data_nascimento': timezone.localdate() - relativedelta(years=random.randint(20, 69)),
            'cpf': str(random.randint(222222, 9999999)),
            'rg': str(random.randint(111111, 9999999)),
            'cartao_sus': str(random.randint(111111, 9999999)),
            'nome_mae': random.choice(['Ana','Maria', 'Antônia']),
            'composicao_familiar': random.randint(1, 10),
            'renda_familiar': random.randint(900, 99999),
            'doenca': random.choice(['Tumores Pituitários', 'Tumores Ósseos',
            'Tumores Neuroendócrinos', 'Tumores Cerebrais/SNC em crinaças']),
            'referencia': random.choice(['Esquina do bar', 'Casa azul', 'Pracinha']),
            'logradouro': random.choice(['Casa', 'Ap']),
            'numero': random.randint(90, 9999),
            'bairro': random.choice(['Campo da água azul', 'Centro', 'Capão redondo']),
            'cidade': random.choice(['Canoinhas', 'Três Barras', 'Curitiba']),
            'raca': 'Preta'
        }
        paciente3 = self.criar_paciente(paciente)

        racas = consulta_racas()
        self.assertIs(racas[0], 5)
        self.assertIs(racas[1], 2)
        self.assertIs(racas[2], 2)
        self.assertIs(racas[3], 1)
        self.assertIs(racas[4], 1)
        self.assertIs(racas[5], 0)

        # Teste 4
        paciente = {
            'nome': 'Lucas',
            'sexo': 'Masculino',
            'data_nascimento': timezone.localdate() - relativedelta(years=random.randint(20, 69)),
            'cpf': str(random.randint(222222, 9999999)),
            'rg': str(random.randint(111111, 9999999)),
            'cartao_sus': str(random.randint(111111, 9999999)),
            'nome_mae': random.choice(['Ana','Maria', 'Antônia']),
            'composicao_familiar': random.randint(1, 10),
            'renda_familiar': random.randint(900, 99999),
            'doenca': random.choice(['Tumores Pituitários', 'Tumores Ósseos',
            'Tumores Neuroendócrinos', 'Tumores Cerebrais/SNC em crinaças']),
            'referencia': random.choice(['Esquina do bar', 'Casa azul', 'Pracinha']),
            'logradouro': random.choice(['Casa', 'Ap']),
            'numero': random.randint(90, 9999),
            'bairro': random.choice(['Campo da água azul', 'Centro', 'Capão redondo']),
            'cidade': random.choice(['Canoinhas', 'Três Barras', 'Curitiba']),
            'raca': 'Não informado'
        }
        paciente4 = self.criar_paciente(paciente)

        racas = consulta_racas()
        self.assertIs(racas[0], 5)
        self.assertIs(racas[1], 2)
        self.assertIs(racas[2], 2)
        self.assertIs(racas[3], 1)
        self.assertIs(racas[4], 1)
        self.assertIs(racas[5], 1)

        # Teste 5
        paciente = {
            'nome': 'Jorge',
            'sexo': 'Masculino',
            'data_nascimento': timezone.localdate() - relativedelta(years=random.randint(20, 69)),
            'cpf': str(random.randint(222222, 9999999)),
            'rg': str(random.randint(111111, 9999999)),
            'cartao_sus': str(random.randint(111111, 9999999)),
            'nome_mae': random.choice(['Ana','Maria', 'Antônia']),
            'composicao_familiar': random.randint(1, 10),
            'renda_familiar': random.randint(900, 99999),
            'doenca': random.choice(['Tumores Pituitários', 'Tumores Ósseos',
            'Tumores Neuroendócrinos', 'Tumores Cerebrais/SNC em crinaças']),
            'referencia': random.choice(['Esquina do bar', 'Casa azul', 'Pracinha']),
            'logradouro': random.choice(['Casa', 'Ap']),
            'numero': random.randint(90, 9999),
            'bairro': random.choice(['Campo da água azul', 'Centro', 'Capão redondo']),
            'cidade': random.choice(['Canoinhas', 'Três Barras', 'Curitiba']),
            'raca': 'Parda'
        }
        paciente5 = self.criar_paciente(paciente)

        racas = consulta_racas()
        self.assertIs(racas[0], 5)
        self.assertIs(racas[1], 2)
        self.assertIs(racas[2], 3)
        self.assertIs(racas[3], 1)
        self.assertIs(racas[4], 1)
        self.assertIs(racas[5], 1)

        # Teste 6
        paciente = {
            'nome': 'Ana',
            'sexo': 'Feminino',
            'data_nascimento': timezone.localdate() - relativedelta(years=random.randint(20, 69)),
            'cpf': str(random.randint(222222, 9999999)),
            'rg': str(random.randint(111111, 9999999)),
            'cartao_sus': str(random.randint(111111, 9999999)),
            'nome_mae': random.choice(['Ana','Maria', 'Antônia']),
            'composicao_familiar': random.randint(1, 10),
            'renda_familiar': random.randint(900, 99999),
            'doenca': random.choice(['Tumores Pituitários', 'Tumores Ósseos',
            'Tumores Neuroendócrinos', 'Tumores Cerebrais/SNC em crinaças']),
            'referencia': random.choice(['Esquina do bar', 'Casa azul', 'Pracinha']),
            'logradouro': random.choice(['Casa', 'Ap']),
            'numero': random.randint(90, 9999),
            'bairro': random.choice(['Campo da água azul', 'Centro', 'Capão redondo']),
            'cidade': random.choice(['Canoinhas', 'Três Barras', 'Curitiba']),
            'raca': 'Amarela'
        }
        paciente6 = self.criar_paciente(paciente)

        racas = consulta_racas()
        self.assertIs(racas[0], 5)
        self.assertIs(racas[1], 2)
        self.assertIs(racas[2], 3)
        self.assertIs(racas[3], 2)
        self.assertIs(racas[4], 1)
        self.assertIs(racas[5], 1)

        # Teste 7
        paciente = {
            'nome': 'Julia',
            'sexo': 'Feminino',
            'data_nascimento': timezone.localdate() - relativedelta(years=random.randint(20, 69)),
            'cpf': str(random.randint(222222, 9999999)),
            'rg': str(random.randint(111111, 9999999)),
            'cartao_sus': str(random.randint(111111, 9999999)),
            'nome_mae': random.choice(['Ana','Maria', 'Antônia']),
            'composicao_familiar': random.randint(1, 10),
            'renda_familiar': random.randint(900, 99999),
            'doenca': random.choice(['Tumores Pituitários', 'Tumores Ósseos',
            'Tumores Neuroendócrinos', 'Tumores Cerebrais/SNC em crinaças']),
            'referencia': random.choice(['Esquina do bar', 'Casa azul', 'Pracinha']),
            'logradouro': random.choice(['Casa', 'Ap']),
            'numero': random.randint(90, 9999),
            'bairro': random.choice(['Campo da água azul', 'Centro', 'Capão redondo']),
            'cidade': random.choice(['Canoinhas', 'Três Barras', 'Curitiba']),
            'raca': 'Branca'
        }
        paciente7 = self.criar_paciente(paciente)

        racas = consulta_racas()
        self.assertIs(racas[0], 6)
        self.assertIs(racas[1], 2)
        self.assertIs(racas[2], 3)
        self.assertIs(racas[3], 2)
        self.assertIs(racas[4], 1)
        self.assertIs(racas[5], 1)

        # Teste 8 - Criando um paciente com uma raça diferente das conhecidas
        paciente = {
            'nome': 'Tadeu',
            'sexo': 'Masculino',
            'data_nascimento': timezone.localdate() - relativedelta(years=random.randint(20, 69)),
            'cpf': str(random.randint(222222, 9999999)),
            'rg': str(random.randint(111111, 9999999)),
            'cartao_sus': str(random.randint(111111, 9999999)),
            'nome_mae': random.choice(['Ana','Maria', 'Antônia']),
            'composicao_familiar': random.randint(1, 10),
            'renda_familiar': random.randint(900, 99999),
            'doenca': random.choice(['Tumores Pituitários', 'Tumores Ósseos',
            'Tumores Neuroendócrinos', 'Tumores Cerebrais/SNC em crinaças']),
            'referencia': random.choice(['Esquina do bar', 'Casa azul', 'Pracinha']),
            'logradouro': random.choice(['Casa', 'Ap']),
            'numero': random.randint(90, 9999),
            'bairro': random.choice(['Campo da água azul', 'Centro', 'Capão redondo']),
            'cidade': random.choice(['Canoinhas', 'Três Barras', 'Curitiba']),
            'raca': 'Teste'
        }
        paciente8 = self.criar_paciente(paciente)

        racas = consulta_racas()
        self.assertIs(racas[0], 6)
        self.assertIs(racas[1], 2)
        self.assertIs(racas[2], 3)
        self.assertIs(racas[3], 2)
        self.assertIs(racas[4], 1)
        self.assertIs(racas[5], 1)

        # Teste 9
        paciente = {
            'nome': 'Amanda',
            'sexo': 'Feminino',
            'data_nascimento': timezone.localdate() - relativedelta(years=random.randint(20, 69)),
            'cpf': str(random.randint(222222, 9999999)),
            'rg': str(random.randint(111111, 9999999)),
            'cartao_sus': str(random.randint(111111, 9999999)),
            'nome_mae': random.choice(['Ana','Maria', 'Antônia']),
            'composicao_familiar': random.randint(1, 10),
            'renda_familiar': random.randint(900, 99999),
            'doenca': random.choice(['Tumores Pituitários', 'Tumores Ósseos',
            'Tumores Neuroendócrinos', 'Tumores Cerebrais/SNC em crinaças']),
            'referencia': random.choice(['Esquina do bar', 'Casa azul', 'Pracinha']),
            'logradouro': random.choice(['Casa', 'Ap']),
            'numero': random.randint(90, 9999),
            'bairro': random.choice(['Campo da água azul', 'Centro', 'Capão redondo']),
            'cidade': random.choice(['Canoinhas', 'Três Barras', 'Curitiba']),
            'raca': 'Preta'
        }
        paciente9 = self.criar_paciente(paciente)

        racas = consulta_racas()
        self.assertIs(racas[0], 6)
        self.assertIs(racas[1], 3)
        self.assertIs(racas[2], 3)
        self.assertIs(racas[3], 2)
        self.assertIs(racas[4], 1)
        self.assertIs(racas[5], 1)

        # Teste 10
        paciente = {
            'nome': 'Igor',
            'sexo': 'Masculino',
            'data_nascimento': timezone.localdate() - relativedelta(years=random.randint(20, 69)),
            'cpf': str(random.randint(222222, 9999999)),
            'rg': str(random.randint(111111, 9999999)),
            'cartao_sus': str(random.randint(111111, 9999999)),
            'nome_mae': random.choice(['Ana','Maria', 'Antônia']),
            'composicao_familiar': random.randint(1, 10),
            'renda_familiar': random.randint(900, 99999),
            'doenca': random.choice(['Tumores Pituitários', 'Tumores Ósseos',
            'Tumores Neuroendócrinos', 'Tumores Cerebrais/SNC em crinaças']),
            'referencia': random.choice(['Esquina do bar', 'Casa azul', 'Pracinha']),
            'logradouro': random.choice(['Casa', 'Ap']),
            'numero': random.randint(90, 9999),
            'bairro': random.choice(['Campo da água azul', 'Centro', 'Capão redondo']),
            'cidade': random.choice(['Canoinhas', 'Três Barras', 'Curitiba']),
            'raca': 'Indígena'
        }
        paciente10 = self.criar_paciente(paciente)

        racas = consulta_racas()
        self.assertIs(racas[0], 6)
        self.assertIs(racas[1], 3)
        self.assertIs(racas[2], 3)
        self.assertIs(racas[3], 2)
        self.assertIs(racas[4], 2)
        self.assertIs(racas[5], 1)


    def test_filtrar_info_gerais(self):
        ''' filtrar_info_gerais(request) '''

        # Mocking a get request
        request = self.factory.get(reverse('pacientes:filtrar_info_gerais'))
        request.user = self.user
        request.GET = request.GET.copy()

        # Teste 1
        request.GET['data_inicio'] = '01/11/2020'
        request.GET['data_fim'] = '30/11/2020'
        request.GET['cidade'] = 'Canoinhas'
        response = filtrar_info_gerais(request)
        self.assertEqual(response.status_code, 200)
        # Conversao para dict
        infos = json.loads(response.content)
        self.assertDictEqual(infos['pacientes'], {"ativos": 4, "inativos": 0, "total": 4})
        self.assertCountEqual(infos['tipo_auxilios'], [{"nome": "Medicamento", "quantidade": 5}, {"nome": "Empréstimo de equipamento", "quantidade": 3}, {"nome": "Cesta básica", "quantidade": 2}, {"nome": "Suplemento alimentar", "quantidade": 4}, {"nome": "Complemento alimentar", "quantidade": 0}, {"nome": "Prótese feminina", "quantidade": 0}, {"nome": "Item de convalescença", "quantidade": 0}])
        self.assertDictEqual(infos['consulta_exame'], {"consulta": 3, "exame": 0})

        # Teste 2
        request.GET['data_inicio'] = '01/12/2020'
        request.GET['data_fim'] = '30/12/2020'
        request.GET['cidade'] = 'Canoinhas'
        response = filtrar_info_gerais(request)
        self.assertEqual(response.status_code, 200)
        infos = json.loads(response.content)

        self.assertDictEqual(infos['pacientes'], {"ativos": 4, "inativos": 0, "total": 4})
        self.assertCountEqual(infos['tipo_auxilios'], [{"nome": "Medicamento", "quantidade": 0}, {"nome": "Empréstimo de equipamento", "quantidade": 0}, {"nome": "Cesta básica", "quantidade": 0}, {"nome": "Suplemento alimentar", "quantidade": 0}, {"nome": "Complemento alimentar", "quantidade": 0}, {"nome": "Prótese feminina", "quantidade": 0}, {"nome": "Item de convalescença", "quantidade": 0}])
        self.assertDictEqual(infos['consulta_exame'], {"consulta": 0, "exame": 0})

        # Teste 3
        request.GET['data_inicio'] = '01/11/2020'
        request.GET['data_fim'] = '30/11/2020'
        request.GET['cidade'] = 'Três Barras'
        response = filtrar_info_gerais(request)
        self.assertEqual(response.status_code, 200)
        infos = json.loads(response.content)
        
        self.assertDictEqual(infos['pacientes'], {"ativos": 2, "inativos": 0, "total": 2})
        self.assertCountEqual(infos['tipo_auxilios'], [{"nome": "Medicamento", "quantidade": 0}, {"nome": "Empréstimo de equipamento", "quantidade": 2}, {"nome": "Cesta básica", "quantidade": 0}, {"nome": "Suplemento alimentar", "quantidade": 0}, {"nome": "Complemento alimentar", "quantidade": 0}, {"nome": "Prótese feminina", "quantidade": 0}, {"nome": "Item de convalescença", "quantidade": 0}])
        self.assertDictEqual(infos['consulta_exame'], {"consulta": 0, "exame": 0})

        # Teste 4 - Criando um novo paciente
        paciente = {
            'nome': 'Gabriel',
            'sexo': 'Masculino',
            'data_nascimento': timezone.localdate() - relativedelta(years=random.randint(20, 69)),
            'cpf': str(random.randint(222222, 9999999)),
            'rg': str(random.randint(111111, 9999999)),
            'cartao_sus': str(random.randint(111111, 9999999)),
            'nome_mae': random.choice(['Ana','Maria', 'Antônia']),
            'composicao_familiar': random.randint(1, 10),
            'renda_familiar': random.randint(900, 99999),
            'doenca': random.choice(['Tumores Pituitários', 'Tumores Ósseos',
            'Tumores Neuroendócrinos', 'Tumores Cerebrais/SNC em crinaças']),
            'referencia': random.choice(['Esquina do bar', 'Casa azul', 'Pracinha']),
            'logradouro': random.choice(['Casa', 'Ap']),
            'numero': random.randint(90, 9999),
            'bairro': random.choice(['Campo da água azul', 'Centro', 'Capão redondo']),
            'cidade': 'Canoinhas',
            'raca': 'Branca'
        }
        paciente1 = self.criar_paciente(paciente)

        request.GET['data_inicio'] = '01/10/2020'
        request.GET['data_fim'] = '30/11/2020'
        request.GET['cidade'] = 'Canoinhas'
        response = filtrar_info_gerais(request)
        self.assertEqual(response.status_code, 200)
        infos = json.loads(response.content)
        
        self.assertDictEqual(infos['pacientes'], {"ativos":5, "inativos": 0, "total": 5})
        self.assertCountEqual(infos['tipo_auxilios'], [{"nome": "Medicamento", "quantidade": 6}, {"nome": "Empréstimo de equipamento", "quantidade": 3}, {"nome": "Cesta básica", "quantidade": 5}, {"nome": "Suplemento alimentar", "quantidade": 5}, {"nome": "Complemento alimentar", "quantidade": 0}, {"nome": "Prótese feminina", "quantidade": 0}, {"nome": "Item de convalescença", "quantidade": 0}])
        self.assertDictEqual(infos['consulta_exame'], {"consulta": 3, "exame": 0})

        # Teste 5 - Criando uma nova consulta
        Consulta.objects.create(
            tipo = TipoConsulta.objects.get(pk=1),
            data = '2020-11-12',
            exames = 'Raio-X',
            paciente = paciente1
        )

        request.GET['data_inicio'] = '01/10/2020'
        request.GET['data_fim'] = '30/11/2020'
        request.GET['cidade'] = 'Canoinhas'
        response = filtrar_info_gerais(request)
        self.assertEqual(response.status_code, 200)
        infos = json.loads(response.content)
        
        self.assertDictEqual(infos['pacientes'], {"ativos":5, "inativos": 0, "total": 5})
        self.assertCountEqual(infos['tipo_auxilios'], [{"nome": "Medicamento", "quantidade": 6}, {"nome": "Empréstimo de equipamento", "quantidade": 3}, {"nome": "Cesta básica", "quantidade": 5}, {"nome": "Suplemento alimentar", "quantidade": 5}, {"nome": "Complemento alimentar", "quantidade": 0}, {"nome": "Prótese feminina", "quantidade": 0}, {"nome": "Item de convalescença", "quantidade": 0}])
        self.assertDictEqual(infos['consulta_exame'], {"consulta": 4, "exame": 0})

        # Teste 6 - Criando um novo exame
        Exame.objects.create(
            tipo = 'Tumografia',
            data = '2020-11-16',
            paciente = Paciente.objects.get(pk=1)
        )

        request.GET['data_inicio'] = '01/10/2020'
        request.GET['data_fim'] = '30/11/2020'
        request.GET['cidade'] = 'Canoinhas'
        response = filtrar_info_gerais(request)
        self.assertEqual(response.status_code, 200)
        infos = json.loads(response.content)
        
        self.assertDictEqual(infos['pacientes'], {"ativos":5, "inativos": 0, "total": 5})
        self.assertCountEqual(infos['tipo_auxilios'], [{"nome": "Medicamento", "quantidade": 6}, {"nome": "Empréstimo de equipamento", "quantidade": 3}, {"nome": "Cesta básica", "quantidade": 5}, {"nome": "Suplemento alimentar", "quantidade": 5}, {"nome": "Complemento alimentar", "quantidade": 0}, {"nome": "Prótese feminina", "quantidade": 0}, {"nome": "Item de convalescença", "quantidade": 0}])
        self.assertDictEqual(infos['consulta_exame'], {"consulta": 4, "exame": 1})

        # Teste 7 - Pesquisando todas as cidades
        request.GET['data_inicio'] = '01/10/2020'
        request.GET['data_fim'] = '30/11/2020'
        request.GET['cidade'] = 'Total'
        response = filtrar_info_gerais(request)
        self.assertEqual(response.status_code, 200)
        infos = json.loads(response.content)
        
        self.assertDictEqual(infos['pacientes'], {"ativos":11, "inativos": 0, "total": 11})
        self.assertCountEqual(infos['tipo_auxilios'], [{"nome": "Medicamento", "quantidade": 10}, {"nome": "Empréstimo de equipamento", "quantidade": 7}, {"nome": "Cesta básica", "quantidade": 8}, {"nome": "Suplemento alimentar", "quantidade": 6}, {"nome": "Complemento alimentar", "quantidade": 0}, {"nome": "Prótese feminina", "quantidade": 0}, {"nome": "Item de convalescença", "quantidade": 0}])
        self.assertDictEqual(infos['consulta_exame'], {"consulta": 6, "exame": 1})

        # Teste 8 - Entregando um auxílio
        Auxilio.objects.create(
            tipo = TipoAuxilio.objects.get(pk=4),
            quantidade = 3,
            data_retirada = '2020-11-03',
            hora_retirada = '13:15:45',
            paciente = Paciente.objects.get(pk=3)
        )

        request.GET['data_inicio'] = '01/11/2020'
        request.GET['data_fim'] = '30/11/2020'
        request.GET['cidade'] = 'Canoinhas'
        response = filtrar_info_gerais(request)
        self.assertEqual(response.status_code, 200)
        infos = json.loads(response.content)
        
        self.assertDictEqual(infos['pacientes'], {"ativos":5, "inativos": 0, "total": 5})
        self.assertCountEqual(infos['tipo_auxilios'], [{"nome": "Medicamento", "quantidade": 5}, {"nome": "Empréstimo de equipamento", "quantidade": 3}, {"nome": "Cesta básica", "quantidade": 2}, {"nome": "Suplemento alimentar", "quantidade": 5}, {"nome": "Complemento alimentar", "quantidade": 0}, {"nome": "Prótese feminina", "quantidade": 0}, {"nome": "Item de convalescença", "quantidade": 0}])
        self.assertDictEqual(infos['consulta_exame'], {"consulta": 4, "exame": 1})

        # Teste 9 - Removendo consulta
        consulta = Consulta.objects.last()
        consulta.delete()

        request.GET['data_inicio'] = '01/11/2020'
        request.GET['data_fim'] = '30/11/2020'
        request.GET['cidade'] = 'Canoinhas'
        response = filtrar_info_gerais(request)
        self.assertEqual(response.status_code, 200)
        infos = json.loads(response.content)
        
        self.assertDictEqual(infos['pacientes'], {"ativos":5, "inativos": 0, "total": 5})
        self.assertCountEqual(infos['tipo_auxilios'], [{"nome": "Medicamento", "quantidade": 5}, {"nome": "Empréstimo de equipamento", "quantidade": 3}, {"nome": "Cesta básica", "quantidade": 2}, {"nome": "Suplemento alimentar", "quantidade": 5}, {"nome": "Complemento alimentar", "quantidade": 0}, {"nome": "Prótese feminina", "quantidade": 0}, {"nome": "Item de convalescença", "quantidade": 0}])
        self.assertDictEqual(infos['consulta_exame'], {"consulta": 3, "exame": 1})

        # Teste 10 - Pesquisando em uma cidade sem resultados
        consulta = Consulta.objects.last()
        consulta.delete()

        request.GET['data_inicio'] = '01/09/2020'
        request.GET['data_fim'] = '30/11/2020'
        request.GET['cidade'] = 'Chapecó'
        response = filtrar_info_gerais(request)
        self.assertEqual(response.status_code, 200)
        infos = json.loads(response.content)
        
        self.assertDictEqual(infos['pacientes'], {"ativos":0, "inativos": 0, "total": 0})
        self.assertCountEqual(infos['tipo_auxilios'], [{"nome": "Medicamento", "quantidade": 0}, {"nome": "Empréstimo de equipamento", "quantidade": 0}, {"nome": "Cesta básica", "quantidade": 0}, {"nome": "Suplemento alimentar", "quantidade": 0}, {"nome": "Complemento alimentar", "quantidade": 0}, {"nome": "Prótese feminina", "quantidade": 0}, {"nome": "Item de convalescença", "quantidade": 0}])
        self.assertDictEqual(infos['consulta_exame'], {"consulta": 0, "exame": 0})

        # Teste 11 - Criando paciente inativo
        paciente = Paciente.objects.create(
            nome = 'Roberta',
            sexo = 'Feminino',
            data_nascimento = '1978-04-17',
            cpf = '143.983.232-12',
            rg = '19323232',
            cartao_sus = '193092003022',
            nome_mae = 'Maria',
            composicao_familiar = 2,
            renda_familiar = 2300,
            doenca = Doenca.objects.get(pk=2),
            referencia = 'Hospital de Canoinhas',
            logradouro = 'Rua Macedo Almeida',
            numero = 2440,
            bairro = 'Água Verde',
            cidade = Cidade.objects.get(pk=1),
            data_cadastro = '2020-11-18',
            raca = 'Branca',
            ativo = False
        )

        request.GET['data_inicio'] = '01/11/2020'
        request.GET['data_fim'] = '30/11/2020'
        request.GET['cidade'] = 'Canoinhas'
        response = filtrar_info_gerais(request)
        self.assertEqual(response.status_code, 200)
        infos = json.loads(response.content)
        
        self.assertDictEqual(infos['pacientes'], {"ativos":5, "inativos": 1, "total": 6})
        self.assertCountEqual(infos['tipo_auxilios'], [{"nome": "Medicamento", "quantidade": 5}, {"nome": "Empréstimo de equipamento", "quantidade": 3}, {"nome": "Cesta básica", "quantidade": 2}, {"nome": "Suplemento alimentar", "quantidade": 5}, {"nome": "Complemento alimentar", "quantidade": 0}, {"nome": "Prótese feminina", "quantidade": 0}, {"nome": "Item de convalescença", "quantidade": 0}])
        self.assertDictEqual(infos['consulta_exame'], {"consulta": 3, "exame": 1})

        # Teste 12 - Desativando um paciente ativo
        paciente1.ativo = False
        paciente1.save()

        request.GET['data_inicio'] = '01/11/2020'
        request.GET['data_fim'] = '30/11/2020'
        request.GET['cidade'] = 'Canoinhas'
        response = filtrar_info_gerais(request)
        self.assertEqual(response.status_code, 200)
        infos = json.loads(response.content)
        
        self.assertDictEqual(infos['pacientes'], {"ativos":4, "inativos": 2, "total": 6})
        self.assertCountEqual(infos['tipo_auxilios'], [{"nome": "Medicamento", "quantidade": 5}, {"nome": "Empréstimo de equipamento", "quantidade": 3}, {"nome": "Cesta básica", "quantidade": 2}, {"nome": "Suplemento alimentar", "quantidade": 5}, {"nome": "Complemento alimentar", "quantidade": 0}, {"nome": "Prótese feminina", "quantidade": 0}, {"nome": "Item de convalescença", "quantidade": 0}])
        self.assertDictEqual(infos['consulta_exame'], {"consulta": 3, "exame": 1})

    # Funcao auxiliar
    def criar_paciente(self, paciente):
        doenca, created = Doenca.objects.get_or_create(nome=paciente['doenca'])
        cidade, created = Cidade.objects.get_or_create(nome=paciente['cidade'])
        paciente = Paciente.objects.create(
            nome = paciente['nome'],
            sexo = paciente['sexo'],
            data_nascimento = paciente['data_nascimento'],
            cpf = paciente['cpf'],
            rg = paciente['rg'],
            cartao_sus = paciente['cartao_sus'],
            nome_mae = paciente['nome_mae'],
            composicao_familiar = paciente['composicao_familiar'],
            renda_familiar = paciente['renda_familiar'],
            doenca = doenca,
            referencia = paciente['referencia'],
            logradouro = paciente['logradouro'],
            numero = paciente['numero'],
            bairro = paciente['bairro'],
            cidade = cidade,
            data_cadastro = timezone.now(),
            raca = paciente['raca'],
        )

        return paciente
