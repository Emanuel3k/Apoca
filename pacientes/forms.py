from django.forms import ModelForm
from django import forms
from .models import *

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Submit, Reset
from crispy_forms.bootstrap import InlineRadios, PrependedText

class FormPaciente(ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'nome', 'sexo', 'cpf', 'data_nascimento', 'rg', 'cartao_sus',
            'nome_mae', 'conjuge', 'profissao', 'casa_propria', 'raca',
            'outros_casos', 'composicao_familiar', 'metastase', 'referencia_doenca',
            'diabetes', 'logradouro', 'numero', 'bairro', 'complemento', 'referencia',
            'cidade', 'cep', 'doenca', 'descricao_metastase', 'data_cadastro',
            'vulnerabilidade_social', 'tipo_auxilio_aprovado', 'orgao_expedidor',
            'observacao_renda'
        ]

    # Renda familiar
    renda_familiar = forms.CharField(max_length=15)

    # Telefone
    ddd_1 = forms.CharField(max_length=3, label='DDD 1')
    ddd_2 = forms.CharField(max_length=3, label='DDD 2', required=False)
    ddd_3 = forms.CharField(max_length=3, label='DDD 3', required=False)
    telefone_1 = forms.CharField(max_length=9)
    telefone_2 = forms.CharField(max_length=9, required=False)
    telefone_3 = forms.CharField(max_length=9, required=False)
    data_nascimento = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=('%d/%m/%Y', )
    )
    data_cadastro = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=('%d/%m/%Y', )
    )

    # Responsavel
    responsavel_1 = forms.CharField(max_length=200, label='Responsável 1', required=False)
    responsavel_2 = forms.CharField(max_length=200, label='Responsável 2', required=False)
    responsavel_3 = forms.CharField(max_length=200, label='Responsável 3', required=False)

    tipo_auxilio_aprovado = forms.ModelMultipleChoiceField(
        queryset=TipoAuxilio.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(FormPaciente, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.attrs = {'novalidate': '', 'enctype': 'multipart/form-data'}
        self.helper.layout = Layout(
            Row(
                HTML('<input type="file" id="btn-foto" name="foto-paciente" onchange="lerURL(this);" class="input-foto" />'),
                HTML('<label for="btn-foto">Escolha uma foto</label>'),
                css_class='justify-content-center mb-2'
            ),
            Row(
                HTML('<button class="btn btn-danger" id="limpar-foto">Limpar foto</button>'),
                css_class='justify-content-center'
            ),
            Row(
                HTML('<h3>Dados básicos</h3>'), css_class='mt-4 mb-3'
            ),
            Row(
                Column('nome', css_class='col-lg-6'),
                Column('data_nascimento', css_class='col-lg-3'),
                Column(InlineRadios('sexo'), css_class='col-lg-3')
            ),
            Row(
                Column('raca', css_class='col-lg-2'),
                Column('cpf', css_class='col-lg-2'),
                Column('rg', css_class='col-lg-2'),
                Column('orgao_expedidor', css_class='col-lg-4'),
                Column('cartao_sus', css_class='col-lg-2')
            ),
            Row(
                Column('nome_mae', css_class='col-lg-4'),
                Column('conjuge', css_class='col-lg-4'),
                Column('ddd_1', css_class='col-lg-1'),
                Column('telefone_1', css_class='col-lg-3'),
            ),
            Row(
                Column('ddd_2', css_class='col-lg-1', required=False),
                Column('telefone_2', css_class='col-lg-3', required=False),
                Column('ddd_3', css_class='col-lg-1', required=False),
                Column('telefone_3', css_class='col-lg-3', required=False),
                Column('data_cadastro', css_class='col-lg-4')
            ),
            Row(
                HTML("<h3>Dados financeiros e familiares</h3>"),
                css_class='mt-4 mb-3'
            ),
            Row(
                Column('profissao', css_class='col-lg-6'),
                Column(PrependedText('renda_familiar', '$'), css_class='col-lg-3'),
                Column('composicao_familiar', css_class='col-lg-3'),
                css_class='align-items-center'
            ),
            Row(
                Column('observacao_renda', css_class='col-lg-6'),
                Column('casa_propria', css_class='col-xl-2 col-lg-3 align-self-end pb-lg-2'),
                Column('outros_casos', css_class='col-xl-2 col-lg-3 align-self-end pb-lg-2'),
                Column('vulnerabilidade_social', css_class='col-xl-2 align-self-end pb-lg-2')
            ),
            Row(
                HTML('<h3>Endereço</h3>'), css_class='mt-4 mb-3'
            ),
            Row(
                Column('logradouro', css_class='col-lg-3'),
                Column('numero', css_class='col-lg-2'),
                Column('bairro', css_class='col-lg-2'),
                Column('complemento', css_class='col-lg-3'),
                Column('cidade', css_class='col-lg-2'),
            ),
            Row(
                Column('cep', css_class='col-lg-2'),
                Column('referencia', css_class='col-lg-10')
            ),
            Row(
                HTML('<h3>Saúde</h3>'),
                css_class='mt-4 mb-3'
            ),
            Row(
                Column('doenca', css_class='col-lg-4'),
                Column('referencia_doenca', css_class='col-lg-8', value=''),
            ),
            Row(
                Column('metastase', css_class='col-lg-2'),
                Column('diabetes', css_class='col-lg-2')
            ),
            Row(
                Column('descricao_metastase', css_class='descricao_metastase d-none')
            ),
            Row(
                HTML('<h3>Responsável</h3>'),
                css_class='mt-4 mb-3'
            ),
            Row(
                Column('responsavel_1', css_class='col-lg-4'),
                Column('responsavel_2', css_class='col-lg-4'),
                Column('responsavel_3', css_class='col-lg-4')
            ),
            Row(
                HTML('<h3>Auxílios aprovados</h3>'),
                css_class='mt-4 mb-3'
            ),
            Row(
                Column('tipo_auxilio_aprovado', css_class='col-12')
            ),
            Row(
                HTML('<button type="button" class="btn btn-danger mb-2 mr-4" data-toggle="modal" data-target="#modal-cancelamento">Cancelar</button>'),
                Submit('submit', 'Cadastrar', css_class='mb-2'),
                css_class='justify-content-end'
            )
        )

class FormAuxilio(ModelForm):
    class Meta:
        model = Auxilio
        fields = [
            'tipo','data_retirada','hora_retirada','observacao','quantidade',
            'medicamento','equipamento','data_devolucao','hora_devolucao',
            'suplemento_alimentar'
        ]

    def __init__(self, *args, **kwargs):
        super(FormAuxilio, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Row(
                HTML('<h3>Dados do auxílio</h3>'), css_class='mt-4 mb-3'
            ),
            Row(
                Column('tipo', css_class='col-md-12')
            ),
            Row(
                Column('medicamento', css_class='col-md-12')
            ),
            Row(
                Column('equipamento', css_class='col-md-12')
            ),
            Row(
                Column('suplemento_alimentar', css_class='col-md-12')
            ),
            Row(
                Column('data_retirada', css_class='col-md-4'),
                Column('hora_retirada', css_class='col-md-4'),
                Column('quantidade', css_class='col-md-4')
            ),
            Row(
                Column('observacao', css_class='col-md-12'),
            ),
            Row(
                HTML('<button type="button" class="btn btn-danger mb-2 mr-4" data-toggle="modal" data-target="#modal-cancelamento">Cancelar</button>'),
                Submit('submit', 'Cadastrar', css_class='mb-2'),
                css_class='justify-content-end'
            )
        )

class FormDevolucao(ModelForm):
    class Meta:
        model = Auxilio
        fields = [
            'data_devolucao','hora_devolucao', 'observacao'
        ]

    def __init__(self, *args, **kwargs):
        super(FormDevolucao, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Row(
                Column('data_devolucao', css_class='col-md-4'),
                Column('hora_devolucao', css_class='col-md-4')
            ),
            Row(
                Column('observacao', css_class='col-md-12'),
            ),
            Row(
                HTML('<button type="button" class="btn btn-danger mb-2 mr-4" data-toggle="modal" data-target="#modal-cancelamento">Cancelar</button>'),
                Submit('submit', 'Cadastrar', css_class='mb-2'),
                css_class='justify-content-end'
            )
        )

class FormMedicamento(ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nome']

    def __init__(self, *args, **kwargs):
        super(FormMedicamento, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Row(
                Column('nome', placeholder='Digite o nome do medicamento', css_class='col-md-12')
            ),
            Row(
                HTML('<button type="button" class="btn btn-danger mb-2 mr-4" data-toggle="modal" data-target="#modal-cancelamento">Cancelar</button>'),
                Submit('submit', 'Cadastrar', css_class='mb-2'),
                css_class='justify-content-end'
            )
        )

class FormEquipamento(ModelForm):
    class Meta:
        model = Equipamento
        fields = ['nome', 'etiqueta']

    def __init__(self, *args, **kwargs):
        super(FormEquipamento, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Row(
                Column('nome', placeholder='Digite o nome do equipamento', css_class='col-md-8'),
                Column('etiqueta', placeholder='Digite a etiqueta do equipamento', css_class='col-md-4')
            ),
            Row(
                HTML('<button type="button" class="btn btn-danger mb-2 mr-4" data-toggle="modal" data-target="#modal-cancelamento">Cancelar</button>'),
                Submit('submit', 'Cadastrar', css_class='mb-2'),
                css_class='justify-content-end'
            )
        )

class FormTipoAuxilio(ModelForm):
    class Meta:
        model = TipoAuxilio
        fields = ['nome', 'abreviacao']

    def __init__(self, *args, **kwargs):
        super(FormTipoAuxilio, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Row(
                Column('nome', placeholder='Digite o nome do auxílio', css_class='col-md-8'),
                Column('abreviacao', placeholder='Digite a abreviação do auxílio', css_class='col-md-4')
            ),
            Row(
                HTML('<button type="button" class="btn btn-danger mb-2 mr-4" data-toggle="modal" data-target="#modal-cancelamento">Cancelar</button>'),
                Submit('submit', 'Cadastrar', css_class='mb-2'),
                css_class='justify-content-end'
            )
        )

class FormCidade(ModelForm):
    class Meta:
        model = Cidade
        fields = ['nome']

    def __init__(self, *args, **kwargs):
        super(FormCidade, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Row(
                Column('nome', placeholder='Digite o nome da cidade', css_class='col-md-12')
            ),
            Row(
                HTML('<button type="button" class="btn btn-danger mb-2 mr-4" data-toggle="modal" data-target="#modal-cancelamento">Cancelar</button>'),
                Submit('submit', 'Cadastrar', css_class='mb-2'),
                css_class='justify-content-end'
            )
        )

class FormTipoConsulta(ModelForm):
    class Meta:
        model = TipoConsulta
        fields = ['nome']

    def __init__(self, *args, **kwargs):
        super(FormTipoConsulta, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Row(
                Column('nome', placeholder='Digite o nome do tipo de consulta', css_class='col-md-12')
            ),
            Row(
                HTML('<button type="button" class="btn btn-danger mb-2 mr-4" data-toggle="modal" data-target="#modal-cancelamento">Cancelar</button>'),
                Submit('submit', 'Cadastrar', css_class='mb-2'),
                css_class='justify-content-end'
            )
        )

class FormConsulta(ModelForm):
    class Meta:
        model = Consulta
        fields = ['tipo', 'data', 'observacao']

    def __init__(self, *args, **kwargs):
        super(FormConsulta, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Row(
                Column('tipo', css_class='col-md-6'),
                Column('data', css_class='col-md-6'),
                Column('observacao', css_class='col-md-12')
            ),
            Row(
                HTML('<button type="button" class="btn btn-danger mb-2 mr-4" data-toggle="modal" data-target="#modal-cancelamento">Cancelar</button>'),
                Submit('submit', 'Cadastrar', css_class='mb-2'),
                css_class='justify-content-end'
            )
        )

class FormExame(ModelForm):
    class Meta:
        model = Exame
        fields = ['tipo', 'data']

    def __init__(self, *args, **kwargs):
        super(FormExame, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Row(
                Column('tipo', placeholder='Digite o nome do tipo de exame', css_class='col-md-8'),
                Column('data', css_class='col-md-4'),
            ),
            Row(
                HTML('<button type="button" class="btn btn-danger mb-2 mr-4" data-toggle="modal" data-target="#modal-cancelamento">Cancelar</button>'),
                Submit('submit', 'Cadastrar', css_class='mb-2'),
                css_class='justify-content-end'
            )
        )

class FormDoenca(ModelForm):
    class Meta:
        model = Doenca
        fields = ['nome']

    def __init__(self, *args, **kwargs):
        super(FormDoenca, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Row(
                Column('nome', placeholder='Digite o nome da doença', css_class='col-md-12')
            ),
            Row(
                HTML('<button type="button" class="btn btn-danger mb-2 mr-4" data-toggle="modal" data-target="#modal-cancelamento">Cancelar</button>'),
                Submit('submit', 'Cadastrar', css_class='mb-2'),
                css_class='justify-content-end'
            )
        )

class FormSuplementoAlimentar(ModelForm):
    class Meta:
        model = SuplementoAlimentar
        fields = ['nome']

    def __init__(self, *args, **kwargs):
        super(FormSuplementoAlimentar, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Row(
                Column('nome', placeholder='Digite o nome do suplemento', css_class='col-md-12')
            ),
            Row(
                HTML('<button type="button" class="btn btn-danger mb-2 mr-4" data-toggle="modal" data-target="#modal-cancelamento">Cancelar</button>'),
                Submit('submit', 'Cadastrar', css_class='mb-2'),
                css_class='justify-content-end'
            )
        )
