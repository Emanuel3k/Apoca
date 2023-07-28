from django.test import TestCase

from pacientes.models import *


class DoencaTestCase(TestCase):

    def setUp(self):
        doenca1 = Doenca.objects.create(nome='Cherophobia')
        doenca2 = Doenca.objects.create(nome='Munchausen syndrome')

    def test_doenca_attrs(self):
        doenca = Doenca.objects.get(nome='Cherophobia')
        self.assertEqual(doenca.nome, 'Cherophobia')
        doenca = Doenca.objects.get(nome='Munchausen syndrome')
        self.assertEqual(doenca.nome, 'Munchausen syndrome')
        # Quantidade
        qtd = Doenca.objects.all().count()
        self.assertIs(qtd, 2)

        # Nova doenca
        doenca3 = Doenca.objects.create(nome='Williams Syndrome')
        doenca = Doenca.objects.get(nome='Williams Syndrome')
        self.assertEqual(doenca.nome, 'Williams Syndrome')
        # Quantidade
        qtd = Doenca.objects.all().count()
        self.assertIs(qtd, 3)


class CidadeTestCase(TestCase):
    """ attrs: nome """

    def setUp(self):
        Cidade1 = Cidade.objects.create(nome='Bêagá')

    def test_Cidade_attrs(self):
        cidade = Cidade.objects.get(nome='Bêagá')
        self.assertEqual(cidade.nome, 'Bêagá')
        # Quantidade
        qtd = Cidade.objects.all().count()
        self.assertIs(qtd, 1)


class TipoAuxilioTestCase(TestCase):
    """ attrs: nome, abreviacao """

    def setUp(self):
        TipoAuxilio1 = TipoAuxilio.objects.create(nome='Direção', abreviacao='DR')
        TipoAuxilio2 = TipoAuxilio.objects.create(nome='Transcrição', abreviacao='TR')

    def test_tipo_auxilio_attrs(self):
        tipo_aux1 = TipoAuxilio.objects.get(nome='Direção')
        self.assertEqual(tipo_aux1.nome, 'Direção')
        tipo_aux2 = TipoAuxilio.objects.get(abreviacao='TR')
        self.assertEqual(tipo_aux2.abreviacao, 'TR')
        # Quantidade
        qtd = TipoAuxilio.objects.all().count()
        self.assertIs(qtd, 2)

        TipoAuxilio3 = TipoAuxilio.objects.create(nome='Psicologia', abreviacao='PS')
        # Quantidade
        qtd = TipoAuxilio.objects.all().count()

        self.assertIs(qtd, 3)


class MedicamentoTestCase(TestCase):
    """ attrs: nome """

    def setUp(self):
        Medicamento1 = Medicamento.objects.create(nome='Doraldina')
        Medicamento2 = Medicamento.objects.create(nome='Paracetamol')

    def test_medicamento_attrs(self):
        med1 = Medicamento.objects.get(nome='Doraldina')
        self.assertEqual(med1.nome, 'Doraldina')
        med2 = Medicamento.objects.get(nome='Paracetamol')
        self.assertEqual(med2.nome, 'Paracetamol')
        # Quantidade
        qtd = Medicamento.objects.all().count()
        self.assertIs(qtd, 2)

        Medicamento3 = Medicamento.objects.create(nome='Dorflex')
        # Quantidade
        qtd = Medicamento.objects.all().count()

        self.assertIs(qtd, 3)


class EquipamentoTestCase(TestCase):
    """ attrs: nome, etiqueta, emprestado """

    def setUp(self):
        Equipamento1 = Equipamento.objects.create(nome='Cadeira de rodas', etiqueta='EQP-01')
        Equipamento2 = Equipamento.objects.create(nome='Peruca', etiqueta='EQP-02', emprestado=True)
        Equipamento3 = Equipamento.objects.create(nome='Muletas', etiqueta='EQP-03', emprestado=False)

    def test_equipamento_attrs(self):
        eqp1 = Equipamento.objects.get(nome='Cadeira de rodas')
        self.assertEqual(eqp1.etiqueta, 'EQP-01')
        eqp2 = Equipamento.objects.get(etiqueta='EQP-03')
        self.assertEqual(eqp2.nome, 'Muletas')
        eqp3 = Equipamento.objects.get(nome='Peruca')
        self.assertIs(eqp3.emprestado, True)
        # Verificando se só existe um equipamento emprestado
        eqps = Equipamento.objects.filter(emprestado=True)
        self.assertIs(len(eqps), 1)

        qtd = Equipamento.objects.all().count()
        self.assertIs(qtd, 3)


class AuxilioTestCase(TestCase):
    """ attrs: tipo, data_retirada, hora_retirada, medicamento, equipamento, quantidade, paciente """

    fixtures = [
        'testes/teste_cidades',
        'doencas',
        'medicamentos',
        'tipo_auxilios',
        'testes/teste_equipamentos',
        'testes/teste_pacientes'
    ]

    def setUp(self):
        entrega1 = Auxilio.objects.create(
            tipo=TipoAuxilio.objects.get(pk=1),
            data_retirada='2020-11-30',
            hora_retirada='15:15',
            medicamento=Medicamento.objects.get(pk=2),
            quantidade=4,
            paciente=Paciente.objects.get(pk=1)
        )
        entrega2 = Auxilio.objects.create(
            tipo=TipoAuxilio.objects.get(pk=3),
            data_retirada='2020-12-05',
            hora_retirada='09:30',
            quantidade=1,
            paciente=Paciente.objects.get(pk=2)
        )

    def test_auxilio_attrs(self):
        auxilio1 = Auxilio.objects.get(tipo_id=1)
        self.assertIs(auxilio1.quantidade, 4)
        self.assertEqual(str(auxilio1.data_retirada), '2020-11-30')

        auxilio2 = Auxilio.objects.get(data_retirada='2020-12-05')
        self.assertEqual(str(auxilio2.hora_retirada), '09:30:00')
        self.assertIs(auxilio2.paciente.id, 2)

        qtd = Auxilio.objects.all().count()
        self.assertIs(qtd, 2)

        entrega3 = Auxilio.objects.create(
            tipo=TipoAuxilio.objects.get(pk=2),
            data_retirada='2020-12-06',
            hora_retirada='10:35',
            equipamento=Equipamento.objects.get(pk=1),
            quantidade=1,
            paciente=Paciente.objects.get(pk=1)
        )

        auxilio3 = Auxilio.objects.get(tipo_id=2)
        self.assertEqual(auxilio3.equipamento.id, 1)
        self.assertEqual(str(auxilio3.data_retirada), '2020-12-06')

        qtd = Auxilio.objects.all().count()
        self.assertIs(qtd, 3)