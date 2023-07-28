from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from ..decorators import *
from ..models import *
from ..forms import *


@assistente_social_required
@login_required
def medicamentos(request):
    if request.method == 'POST':
        try:
            medicamento = get_object_or_404(Medicamento, pk=request.POST['pk'])
            medicamento.delete()
        except Exception:
            messages.error(request, 'O medicamento não pode ser deletado pois tem relação com um ou mais pacientes.')
        else:
            messages.success(request, 'Medicamento excluído com sucesso!')

    medicamentos = Medicamento.objects.all()
    return render(request, 'cadastros_gerais/medicamento/medicamento.html', {'medicamentos': medicamentos})


@assistente_social_required
@login_required
def cadastrar_medicamento(request):
    form = FormMedicamento(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            medicamento_repetido = Medicamento.objects.filter(nome=form.cleaned_data['nome'])
            if medicamento_repetido:
                messages.error(request, 'O medicamento informado já existe.')
            else:
                form.save()
                messages.success(request, 'Medicamento cadastrado com sucesso!')
                return redirect('pacientes:medicamentos')

    return render(request, 'cadastros_gerais/medicamento/cadastro_medicamento.html', {'form': form})


@assistente_social_required
@login_required
def editar_medicamento(request, pk):
    medicamento = get_object_or_404(Medicamento, pk=pk)
    nome = medicamento.nome

    if request.method == 'POST':
        form = FormMedicamento(request.POST, instance=medicamento)
        if form.is_valid():
            medicamento_repetido = Medicamento.objects.filter(nome=form.cleaned_data['nome'])

            if medicamento_repetido and medicamento_repetido[0].nome == form.cleaned_data['nome'] and nome != form.cleaned_data['nome'] :
                messages.error(request, 'O medicamento informado já existe.')
            else:
                form.save()
                messages.success(request, 'Medicamento editado com sucesso!')
                return redirect('pacientes:medicamentos')
    else:
        form = FormMedicamento(instance=medicamento)

    return render(request, 'cadastros_gerais/medicamento/edicao_medicamento.html', {'form': form})


@assistente_social_required
@login_required
def equipamentos(request):
    if request.method == 'POST':
        try:
            equipamento = get_object_or_404(Equipamento, pk=request.POST['pk'])
            equipamento.delete()
        except Exception:
            messages.error(request, 'O equipamento não pode ser deletado pois tem relação com um ou mais pacientes.')
        else:
            messages.success(request, 'Equipamento excluído com sucesso!')

    equipamentos = Equipamento.objects.all()
    return render(request, 'cadastros_gerais/equipamento/equipamento.html', {'equipamentos': equipamentos})


@assistente_social_required
@login_required
def cadastrar_equipamento(request):
    form = FormEquipamento(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            equipamento_repetido = Equipamento.objects.filter(etiqueta=form.cleaned_data['etiqueta'])
            if equipamento_repetido:
                messages.error(request, 'A etiqueta informada já foi cadastrada.')
            else:
                form.save()
                messages.success(request, 'Equipamento cadastrado com sucesso!')
                return redirect('pacientes:equipamentos')

    return render(request, 'cadastros_gerais/equipamento/cadastro_equipamento.html', {'form': form})


@assistente_social_required
@login_required
def editar_equipamento(request, pk):
    equipamento = get_object_or_404(Equipamento, pk=pk)
    etiqueta = equipamento.etiqueta

    if request.method == 'POST':
        form = FormEquipamento(request.POST, instance=equipamento)
        if form.is_valid():
            equipamento_repetido = Equipamento.objects.filter(etiqueta=form.cleaned_data['etiqueta'])

            if equipamento_repetido and equipamento_repetido[0].etiqueta == form.cleaned_data['etiqueta'] and form.cleaned_data['etiqueta'] != etiqueta:
                messages.error(request, 'O equipamento informado já existe.')
            else:
                form.save()
                messages.success(request, 'Equipamento editado com sucesso!')
                return redirect('pacientes:equipamentos')
    else:
        form = FormEquipamento(instance=equipamento)

    return render(request, 'cadastros_gerais/equipamento/edicao_equipamento.html', {'form': form})


@assistente_social_required
@login_required
def tipos_auxilios(request):
    if request.method == 'POST':
        try:
            tipo_auxilio = get_object_or_404(TipoAuxilio, pk=request.POST['pk'])
            tipo_auxilio.delete()
        except Exception:
            messages.error(request, 'O tipo de auxílio não pode ser deletado pois tem relação com um ou mais pacientes.')
        else:
            messages.success(request, 'Tipo de auxílio excluído com sucesso!')

    tipo_auxilios = TipoAuxilio.objects.all()
    return render(request, 'cadastros_gerais/tipo_auxilio/tipo_auxilio.html', {'tipos_auxilios': tipo_auxilios})


@assistente_social_required
@login_required
def cadastrar_tipo_auxilio(request):
    form = FormTipoAuxilio(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            auxilio_repetido = TipoAuxilio.objects.filter(nome=form.cleaned_data['nome'])
            if auxilio_repetido:
                messages.error(request, 'O tipo de auxílio informado já foi cadastrado.')
            else:
                form.save()
                messages.success(request, 'Tipo de auxílio cadastrado com sucesso!')
                return redirect('pacientes:tipos_auxilios')

    return render(request, 'cadastros_gerais/tipo_auxilio/cadastro_tipo_auxilio.html', {'form': form})


@assistente_social_required
@login_required
def editar_tipo_auxilio(request, pk):
    tipo_auxilio = get_object_or_404(TipoAuxilio, pk=pk)
    nome = tipo_auxilio.nome

    if request.method == 'POST':
        form = FormTipoAuxilio(request.POST, instance=tipo_auxilio)
        if form.is_valid():
            tipo_auxilio_repetido = TipoAuxilio.objects.filter(nome=form.cleaned_data['nome'])

            if tipo_auxilio_repetido and tipo_auxilio_repetido[0].nome == form.cleaned_data['nome'] and form.cleaned_data['nome'] != nome:
                messages.error(request, 'O tipo de auxílio informado já existe.')
            else:
                form.save()
                messages.success(request, 'Tipo de auxílio editado com sucesso!')
                return redirect('pacientes:tipos_auxilios')
    else:
        form = FormTipoAuxilio(instance=tipo_auxilio)

    return render(request, 'cadastros_gerais/tipo_auxilio/edicao_tipo_auxilio.html', {'form': form})


@assistente_social_required
@login_required
def cidades(request):
    if request.method == 'POST':
        try:
            cidade = get_object_or_404(Cidade, pk=request.POST['pk'])
            cidade.delete()
        except Exception:
            messages.error(request, 'A cidade não pode ser deletado pois tem relação com um ou mais pacientes.')
        else:
            messages.success(request, 'Cidade excluída com sucesso!')

    cidades = Cidade.objects.all()
    return render(request, 'cadastros_gerais/cidade/cidade.html', {'cidades': cidades})


@assistente_social_required
@login_required
def cadastrar_cidade(request):
    form = FormCidade(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            cidade_repetida = Cidade.objects.filter(nome=form.cleaned_data['nome'])
            if cidade_repetida:
                messages.error(request, 'A cidade informada já foi cadastrada.')
            else:
                form.save()
                messages.success(request, 'Cidade cadastrada com sucesso!')
                return redirect('pacientes:cidades')

    return render(request, 'cadastros_gerais/cidade/cadastro_cidade.html', {'form': form})


@assistente_social_required
@login_required
def editar_cidade(request, pk):
    cidade = get_object_or_404(Cidade, pk=pk)
    nome = cidade.nome

    if request.method == 'POST':
        form = FormCidade(request.POST, instance=cidade)
        if form.is_valid():
            cidade_repetida = Cidade.objects.filter(nome=form.cleaned_data['nome'])

            if cidade_repetida and cidade_repetida[0].nome == form.cleaned_data['nome'] and form.cleaned_data['nome'] != nome:
                messages.error(request, 'A cidade informada já existe.')
            else:
                form.save()
                messages.success(request, 'Cidade editada com sucesso!')
                return redirect('pacientes:cidades')
    else:
        form = FormCidade(instance=cidade)

    return render(request, 'cadastros_gerais/cidade/edicao_cidade.html', {'form': form})


@assistente_social_required
@login_required
def tipos_consulta(request):
    if request.method == 'POST':
        try:
            tipo_consulta = get_object_or_404(TipoConsulta, pk=request.POST['pk'])
            tipo_consulta.delete()
        except Exception:
            messages.error(request, 'O tipo de consulta não pode ser deletado pois tem relação com um ou mais pacientes.')
        else:
            messages.success(request, 'Tipo de consulta excluído com sucesso!')

    tipos_consulta = TipoConsulta.objects.all()
    return render(request, 'cadastros_gerais/tipo_consulta/tipo_consulta.html', {'tipos_consulta': tipos_consulta})


@assistente_social_required
@login_required
def cadastrar_tipo_consulta(request):
    form = FormTipoConsulta(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            tipo_repetido = TipoConsulta.objects.filter(nome=form.cleaned_data['nome'])
            if tipo_repetido:
                messages.error(request, 'O tipo de consulta informado já foi cadastrado.')
            else:
                form.save()
                messages.success(request, 'Tipo de consulta cadastrado com sucesso!')
                return redirect('pacientes:tipos_consulta')

    return render(request, 'cadastros_gerais/tipo_consulta/cadastro_tipo_consulta.html', {'form': form})


@assistente_social_required
@login_required
def editar_tipo_consulta(request, pk):
    tipo_consulta = get_object_or_404(TipoConsulta, pk=pk)
    nome = tipo_consulta.nome

    if request.method == 'POST':
        form = FormTipoConsulta(request.POST, instance=tipo_consulta)
        if form.is_valid():
            tipo_consulta_repetido = TipoConsulta.objects.filter(nome=form.cleaned_data['nome'])

            if tipo_consulta_repetido and tipo_consulta_repetido[0].nome == form.cleaned_data['nome'] and form.cleaned_data['nome'] != nome:
                messages.error(request, 'O tipo de consulta informado já existe.')
            else:
                form.save()
                messages.success(request, 'Tipo de consulta editado com sucesso!')
                return redirect('pacientes:tipos_consulta')
    else:
        form = FormTipoConsulta(instance=tipo_consulta)

    return render(request, 'cadastros_gerais/tipo_consulta/edicao_tipo_consulta.html', {'form': form})

@assistente_social_required
@login_required
def doencas(request):
    if request.method == 'POST':
        try:
            doenca = get_object_or_404(Doenca, pk=request.POST['pk'])
            doenca.delete()
        except Exception:
            messages.error(request, 'A doença não pode ser deletada pois tem relação com um ou mais pacientes.')
        else:
            messages.success(request, 'Doença excluída com sucesso!')

    doencas = Doenca.objects.all()
    return render(request, 'cadastros_gerais/doenca/doenca.html', {'doencas': doencas})


@assistente_social_required
@login_required
def cadastrar_doenca(request):
    form = FormDoenca(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            doenca_repetida = Doenca.objects.filter(nome=form.cleaned_data['nome'])
            if doenca_repetida:
                messages.error(request, 'A doença informada já foi cadastrada.')
            else:
                form.save()
                messages.success(request, 'Doença cadastrada com sucesso!')
                return redirect('pacientes:doencas')

    return render(request, 'cadastros_gerais/doenca/cadastro_doenca.html', {'form': form})


@assistente_social_required
@login_required
def editar_doenca(request, pk):
    doenca = get_object_or_404(Doenca, pk=pk)
    nome = doenca.nome

    if request.method == 'POST':
        form = FormDoenca(request.POST, instance=doenca)
        if form.is_valid():
            doenca_repetida = Doenca.objects.filter(nome=form.cleaned_data['nome'])

            if doenca_repetida and doenca_repetida[0].nome == form.cleaned_data['nome'] and form.cleaned_data['nome'] != nome:
                messages.error(request, 'A doença informada já existe.')
            else:
                form.save()
                messages.success(request, 'Doença editada com sucesso!')
                return redirect('pacientes:doencas')
    else:
        form = FormDoenca(instance=doenca)

    return render(request, 'cadastros_gerais/doenca/edicao_doenca.html', {'form': form})

@assistente_social_required
@login_required
def sup_alimentares(request):
    if request.method == 'POST':
        try:
            suplemento = get_object_or_404(SuplementoAlimentar, pk=request.POST['pk'])
            suplemento.delete()
        except Exception:
            messages.error(request, 'O suplemento alimentar não pode ser deletado pois tem relação com um ou mais pacientes.')
        else:
            messages.success(request, 'Suplemento alimentar excluído com sucesso!')

    suplementos = SuplementoAlimentar.objects.all()
    return render(request, 'cadastros_gerais/sup_alimentar/sup_alimentar.html', {'suplementos': suplementos})


@assistente_social_required
@login_required
def cadastrar_sup_alimentar(request):
    form = FormSuplementoAlimentar(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            suplemento_repetido = SuplementoAlimentar.objects.filter(nome=form.cleaned_data['nome'])
            if suplemento_repetido:
                messages.error(request, 'O suplemento alimentar informado já foi cadastrado.')
            else:
                form.save()
                messages.success(request, 'Suplemento cadastrado com sucesso!')
                return redirect('pacientes:sup_alimentares')

    return render(request, 'cadastros_gerais/sup_alimentar/cadastro_sup_alimentar.html', {'form': form})


@assistente_social_required
@login_required
def editar_sup_alimentar(request, pk):
    suplemento = get_object_or_404(SuplementoAlimentar, pk=pk)
    nome = suplemento.nome

    if request.method == 'POST':
        form = FormSuplementoAlimentar(request.POST, instance=suplemento)
        if form.is_valid():
            suplemento_repetido = SuplementoAlimentar.objects.filter(nome=form.cleaned_data['nome'])

            if suplemento_repetido and suplemento_repetido[0].nome == form.cleaned_data['nome'] and form.cleaned_data['nome'] != nome:
                messages.error(request, 'O suplemento alimentar informado já existe.')
            else:
                form.save()
                messages.success(request, 'Suplemento alimentar editado com sucesso!')
                return redirect('pacientes:sup_alimentares')
    else:
        form = FormSuplementoAlimentar(instance=suplemento)

    return render(request, 'cadastros_gerais/sup_alimentar/edicao_sup_alimentar.html', {'form': form})