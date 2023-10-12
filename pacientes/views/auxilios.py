from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.forms import ModelChoiceField
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from ..decorators import *
from ..models import *
from ..forms import *
from .utilitarios import *


@assistente_social_required
@login_required
def listar_auxilios(request):
    if request.method == 'POST':
        try:
            auxilio = get_object_or_404(Auxilio, pk=request.POST['pk'])
            auxilio.delete()
        except Exception:
            messages.error(request, 'O auxílio não pode ser excluído.')
        else:
            messages.success(request, 'Auxílio excluído com sucesso!')

    lista_auxilios = Auxilio.objects.all().order_by('data_retirada')

    return render(request, 'auxilios/lista_auxilios.html', {'lista_auxilios': lista_auxilios})


@assistente_social_required
@login_required
def cadastrar_auxilio(request, pk):
    form_auxilio = FormAuxilio(request.POST or None)
    form_auxilio.fields['equipamento'] = ModelChoiceField(queryset=Equipamento.objects.filter(emprestado=False))
    print(form_auxilio.fields['equipamento'])
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == "POST":
        if form_auxilio.is_valid():
            auxilio = form_auxilio.save(commit=False)
            if str(auxilio.tipo.nome).upper() == 'MEDICAMENTO':
                if auxilio.medicamento is None:
                    messages.error(request, 'Erro. Selecione um medicamento ou altere o tipo do auxílio.')
                    return render(request, 'auxilios/cadastro_auxilio.html', {'form': form_auxilio})
            else:
                auxilio.medicamento = None
            if str(auxilio.tipo.nome).upper() == 'EMPRÉSTIMO DE EQUIPAMENTO':
                if auxilio.equipamento is None:
                    messages.error(request, 'Erro. Selecione um equipamento ou altere o tipo do auxílio.')
                    return render(request, 'auxilios/cadastro_auxilio.html', {'form': form_auxilio})
                else:
                    equipamento = get_object_or_404(Equipamento, pk=auxilio.equipamento.id)
                    if(equipamento.emprestado):
                        messages.error(request, 'Equipamento já está emprestado.')
                        return render(request, 'auxilios/cadastro_auxilio.html', {'form': form_auxilio})
                    else:
                        equipamento.emprestado = True
                        equipamento.save()
            else:
                auxilio.equipamento = None
            
            if str(auxilio.tipo.nome).upper() == 'SUPLEMENTO ALIMENTAR':
                if auxilio.suplemento_alimentar is None:
                    messages.error(request, 'Erro. Selecione um suplemento alimentar ou altere o tipo do auxílio.')
                    return render(request, 'auxilios/cadastro_auxilio.html', {'form': form_auxilio})
            else:
                auxilio.suplemento_alimentar = None

            auxilio.paciente = get_object_or_404(Paciente, pk=pk)
            auxilio.save()

            messages.success(request, 'Auxílio cadastrado com sucesso.')
            return redirect('pacientes:perfil_paciente', pk=auxilio.paciente.pk)

        messages.error(request, 'Não foi possível cadastrar o auxílio.')

    return render(request, 'auxilios/cadastro_auxilio.html', {'form': form_auxilio, 'paciente': paciente})


@assistente_social_required
@login_required
def editar_auxilio(request, pk):
    auxilio = get_object_or_404(Auxilio, pk=pk)
    if request.method == 'POST':
        form_auxilio = FormAuxilio(request.POST, instance=auxilio)
        if form_auxilio.is_valid():
            auxilio = form_auxilio.save(commit=False)
            if str(auxilio.tipo.abreviacao) == 'ME':
                if auxilio.medicamento is None:
                    messages.error(request, 'Erro. Selecione um medicamento ou altere o tipo do auxílio.')
                    return render(request, 'auxilios/edicao_auxilio.html', {'form': form_auxilio})
            else:
                auxilio.medicamento = None
            if str(auxilio.tipo.abreviacao) == 'EE':
                if auxilio.equipamento is None:
                    messages.error(request, 'Erro. Selecione um equipamento ou altere o tipo do auxílio.')
                    return render(request, 'auxilios/edicao_auxilio.html', {'form': form_auxilio})
            else:
                auxilio.equipamento = None

            auxilio.save()

            messages.success(request, 'Auxílio alterado com sucesso.')
            return redirect('pacientes:listar_auxilios')
    else:
        auxilio.data_retirada = None
        auxilio.hora_retirada = None
        form_auxilio = FormAuxilio(instance=auxilio)

    return render(request, 'auxilios/edicao_auxilio.html', {'form': form_auxilio, 'paciente': auxilio.paciente})


@assistente_social_required
@login_required
def listar_equipamentos_emprestados(request):
    equipamentos_emprestados = Auxilio.objects.all().filter(tipo__abreviacao='EE',
        data_devolucao__isnull=True, equipamento__emprestado=True).order_by('-data_retirada')

    return render(request, 'auxilios/equipamentos_emprestados.html', {'equipamentos_emprestados': equipamentos_emprestados})


@assistente_social_required
@login_required
def registrar_devolucao(request, pk):
    auxilio = get_object_or_404(Auxilio, pk=pk)
    if request.method == 'POST':
        form_auxilio = FormDevolucao(request.POST, instance=auxilio)
        if form_auxilio.is_valid():
            if auxilio.equipamento.emprestado:
                if auxilio.data_devolucao is None:
                    messages.error(request, 'Informe a data de devolução.')
                elif auxilio.hora_devolucao is None:
                    messages.error(request, 'Informe a hora de devolução.')
                else:
                    auxilio.equipamento.emprestado = False
                    auxilio.equipamento.save()
                    messages.success(request, 'Devolução registrada com sucesso!')
                    return redirect('pacientes:listar_equipamentos_emprestados')
            else:
                messages.error(request, 'Equipamento não estava emprestado.')
        else:
            messages.error(request, 'Erro ao validar formulário.')
    else:
        auxilio.data_devolucao = None
        form_auxilio = FormDevolucao(instance=auxilio)

    return render(request, 'auxilios/registro_devolucao.html', {'form': form_auxilio, 'auxilio': auxilio})

@assistente_social_required
@login_required
def renovar_emprestimo(request, pk):
    auxilio_antigo = get_object_or_404(Auxilio, pk=pk)
    auxilio_antigo.data_devolucao = datetime.today().strftime('%Y-%m-%d')
    auxilio_antigo.hora_devolucao = datetime.today().strftime('%H:%M:%S')

    auxilio = Auxilio()
    auxilio.tipo = auxilio_antigo.tipo
    auxilio.data_retirada = datetime.today().strftime('%Y-%m-%d')
    auxilio.hora_retirada = datetime.today().strftime('%H:%M:%S')
    auxilio.observacao = auxilio_antigo.observacao
    auxilio.quantidade = auxilio_antigo.quantidade
    auxilio.equipamento = auxilio_antigo.equipamento
    auxilio.tipo = auxilio_antigo.tipo
    auxilio.paciente = auxilio_antigo.paciente

    auxilio.save()
    auxilio_antigo.save()
    
    return redirect("/")



@login_required
def detalhes_auxilio(request, pk):
    auxilio = get_object_or_404(Auxilio, pk=pk)
    return render(request, 'auxilios/detalhes_auxilio.html', {'auxilio': auxilio})