from django.db import models
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import MinValueValidator

from PIL import Image
from io import BytesIO
import sys


class Paciente(models.Model):
    SEXO_CHOICES = (
        ('Masculino', 'Masculino'),
        ('Feminino', 'Feminino'),
        ('Outro', 'Outro'),
        ("nulo", "nulo")
    )

    RACA_CHOICES = (
        ('Branca', 'Branca'),
        ('Preta', 'Preta'),
        ('Parda', 'Parda'),
        ('Amarela', 'Amarela'),
        ('Indígena', 'Indígena'),
        ('Não informado', 'Não informado')
    )

    foto = models.ImageField(blank=True, null=True, upload_to='fotos/%Y/')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    # Dados Gerais
    nome = models.CharField(max_length=150)
    sexo = models.CharField(max_length=15, choices=SEXO_CHOICES, default='Masculino')
    data_nascimento = models.DateField('Data de nascimento')
    raca = models.CharField('Raça', max_length=20, choices=RACA_CHOICES, default='Não informado')
    cpf = models.CharField('CPF', max_length=14)
    rg = models.CharField('RG', max_length=9)
    orgao_expedidor = models.CharField('Orgão expedidor', max_length=300, blank=True, null=True)
    cartao_sus = models.CharField('Cartão SUS', max_length=20, blank=True, null=True)
    nome_mae = models.CharField('Nome da mãe', max_length=150)
    conjuge = models.CharField('Cônjuge', max_length=150, blank=True, null=True)
    # Financeiro e Familiar
    profissao = models.CharField('Profissão', max_length=50, blank=True, null=True)
    casa_propria = models.BooleanField('Casa própria', default=False)
    outros_casos = models.BooleanField(default=False)
    composicao_familiar = models.PositiveIntegerField('Composição familiar')
    renda_familiar = models.FloatField('Renda familiar', default=0, validators=[MinValueValidator(0)])
    vulnerabilidade_social = models.BooleanField('Vulnerabilidade social', default=False)
    observacao_renda = models.CharField('Observação', max_length=300, blank=True, null=True) 
    # Doenca
    doenca = models.ForeignKey('Doenca', on_delete=models.PROTECT, verbose_name='Diagnóstico')
    metastase = models.BooleanField('Metástase', default=False)
    descricao_metastase = models.CharField('Localização metástase', max_length=200, blank=True, null=True)
    diabetes = models.BooleanField(default=False)
    referencia_doenca = models.CharField('Referência hospitalar', max_length=150, default='')
    # Endereco
    logradouro = models.CharField(max_length=100)
    numero = models.PositiveIntegerField('Número', blank=True, null=True, validators=[MinValueValidator(0)])
    bairro = models.CharField(max_length=50)
    cidade = models.ForeignKey('Cidade', on_delete=models.PROTECT)
    cep = models.CharField('CEP', max_length=9)
    complemento = models.CharField(max_length=50, blank=True, null=True)
    referencia = models.CharField('Ponto de referência', max_length=200, blank=True, null=True)
    # Demais informacoes
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateField('Data de cadastro')
    tipo_auxilio_aprovado = models.ManyToManyField('pacientes.TipoAuxilio', blank=True)
    paciente = models.BooleanField(default=True)
    comodatario = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if self.foto:
            im = Image.open(self.foto)
            output = BytesIO()
            im.thumbnail((512, 512), Image.ANTIALIAS)

            im.save(output, format='JPEG', quality=80)
            output.seek(0)

            self.foto = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.foto.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

        super(Paciente, self).save()

    def renda_per_capita(self):
        return self.renda_familiar / self.composicao_familiar

    def converter_renda_familiar(self, renda):
        renda = renda.replace('.', '').replace(',', '.')
        self.renda_familiar = float(renda)


class Doenca(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']


class Cidade(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']


class Telefone(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='telefones')
    ddd = models.CharField(max_length=3)
    telefone = models.CharField(max_length=9)

    def __str__(self):
        return ('({}) {}' .format(self.ddd, self.telefone))


class Responsavel(models.Model):
    paciente = models.ForeignKey("Paciente", on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

    class Meta():
        verbose_name_plural = 'responsáveis'


class Medicamento(models.Model):
    nome = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']


class Equipamento(models.Model):
    etiqueta = models.CharField(max_length=50, blank=True, null=True)
    nome = models.CharField(max_length=200, blank=False, null=False)
    emprestado = models.BooleanField(blank=False, null=False, default=False)
    quantidade = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']

class SuplementoAlimentar(models.Model):
    nome = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']

class TipoAuxilio(models.Model):
    nome = models.CharField(max_length=200, blank=False, null=False)
    abreviacao = models.CharField('Abreviação', max_length=5, blank=False, null=False)

    def __str__(self):
        return self.nome


class Auxilio(models.Model):
    tipo = models.ForeignKey(TipoAuxilio, on_delete=models.PROTECT)
    data_retirada = models.DateField(blank=False, null=False)
    hora_retirada = models.TimeField(blank=True, null=True)
    observacao = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Observações')
    quantidade = models.PositiveIntegerField(blank=False, null=False, validators=[MinValueValidator(1)])
    medicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT,
        blank=True, null=True, default=None, related_name='medicamentos')
    equipamento = models.ForeignKey(Equipamento, on_delete=models.PROTECT,
        blank=True, null=True, default=None, related_name='equipamentos')
    suplemento_alimentar = models.ForeignKey(SuplementoAlimentar, on_delete=models.PROTECT,
        blank=True, null=True, default=None, related_name='suplementos')
    data_devolucao = models.DateField(blank=True, null=True, verbose_name='Data Devolução')
    hora_devolucao = models.TimeField(blank=True, null=True, verbose_name='Hora Devolução')
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT,
        blank=True, null=True, default=None, related_name='auxilios')

    def __str__(self):
        if self.medicamento:
            return f'{self.tipo.nome} ({self.medicamento})'
        elif self.equipamento:
            return f'{self.tipo.nome} ({self.equipamento})'
        elif self.suplemento_alimentar:
            return f'{self.tipo.nome} ({self.suplemento_alimentar})'
        else:
            return f'{self.tipo.nome}'


class TipoConsulta(models.Model):
    nome = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.nome


class Consulta(models.Model):
    tipo = models.ForeignKey(TipoConsulta, on_delete=models.PROTECT)
    data = models.DateField(blank=False, null=False)
    observacao = models.TextField(blank=True, null=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.tipo.nome} - ({self.paciente})'


class Exame(models.Model):
    tipo = models.CharField(max_length=250, blank=False, null=False)
    data = models.DateField(blank=False, null=False)
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.tipo} - ({self.paciente})'
