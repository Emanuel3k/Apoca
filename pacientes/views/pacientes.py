from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count

from ..decorators import *
from ..models import *
from ..forms import *
from .utilitarios import *
from .inicio import *
from .consultas_perfil import *

from datetime import datetime
import locale


@login_required
def pacientes(request):
    pacientes = Paciente.objects.filter(ativo=True).order_by('nome').annotate(qtd_auxilio=Count('tipo_auxilio_aprovado') - 3)
    paciente_sexo = (
        Paciente.objects.filter(sexo='Masculino').count(),
        Paciente.objects.filter(sexo='Feminino').count(),
        Paciente.objects.filter(sexo='Outro').count()
    )

    cidades = Cidade.objects.annotate(quantidade=Count('paciente'))
    doencas_comuns = Doenca.objects.annotate(quantidade=Count('paciente')).order_by('-quantidade')[:5]

    return render(request, 'pacientes/lista_paciente.html', {
        'pacientes': pacientes,  'cidades': cidades,
        'paciente_sexo': paciente_sexo, 'doencas_comuns': doencas_comuns
    })


@assistente_social_required
@login_required
def cadastrar_paciente(request):
    form = FormPaciente(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            paciente_repetido = Paciente.objects.filter(cpf=form.cleaned_data['cpf'])
            if paciente_repetido:
                messages.error(request, 'O CPF informado já está cadastrado no sistema.')
            else:
                paciente = form.save(commit=False)

                paciente.converter_renda_familiar(form.cleaned_data['renda_familiar'])

                # Verifica se houve um upload de foto
                if request.FILES.get('foto-paciente'):
                    paciente.foto = request.FILES['foto-paciente']

                paciente.save()
                form.save_m2m()

                cadastrar_telefone(form.cleaned_data['ddd_1'], form.cleaned_data['telefone_1'], paciente)
                cadastrar_telefone(form.cleaned_data['ddd_2'], form.cleaned_data['telefone_2'], paciente)
                cadastrar_telefone(form.cleaned_data['ddd_3'], form.cleaned_data['telefone_3'], paciente)
                cadastrar_responsavel(form.cleaned_data['responsavel_1'], paciente)
                cadastrar_responsavel(form.cleaned_data['responsavel_2'], paciente)
                cadastrar_responsavel(form.cleaned_data['responsavel_3'], paciente)

                messages.success(request, 'Paciente cadastrado(a) com sucesso.')
                return redirect('pacientes:inicio')

        messages.error(request, 'Não foi possível cadastrar o(a) paciente.')

    return render(request, 'pacientes/cadastro_paciente.html', {'form': form})


@assistente_social_required
@login_required
def editar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)

    if request.method == 'POST':
        form = FormPaciente(request.POST, request.FILES, instance=paciente)
        if form.is_valid():
            paciente = form.save(commit=False)

            paciente.converter_renda_familiar(form.cleaned_data['renda_familiar'])

            # Verifica se houve um upload de foto
            if request.FILES.get('foto-paciente'):
                paciente.foto = request.FILES['foto-paciente']
            else:
                # Caso o paciente não tenha foto previamente cadastrada
                # (para evitar de apagar a foto já existente)
                if not paciente.foto:
                    paciente.foto = None

            paciente.save()
            form.save_m2m()

            telefones = [
                {'ddd': form.cleaned_data['ddd_1'], 'telefone': form.cleaned_data['telefone_1']},
                {'ddd': form.cleaned_data['ddd_2'], 'telefone': form.cleaned_data['telefone_2']},
                {'ddd': form.cleaned_data['ddd_3'], 'telefone': form.cleaned_data['telefone_3']},
            ]
            editar_telefones(telefones, paciente)

            responsaveis = [
                form.cleaned_data['responsavel_1'],
                form.cleaned_data['responsavel_2'],
                form.cleaned_data['responsavel_3'],
            ]
            editar_responsaveis(responsaveis, paciente)

            messages.success(request, 'Paciente editado(a) com sucesso.')
            return redirect('pacientes:pacientes')
        else:
            messages.error(request, 'Não foi possível editar o(a) paciente.')
    else:
        dados = {}

        dados['renda_familiar'] = paciente.renda_familiar

        telefones = Telefone.objects.filter(paciente=paciente)
        dados['ddd_1'] = telefones[0].ddd if 0 < len(telefones) else None
        dados['ddd_2'] = telefones[1].ddd if 1 < len(telefones) else None
        dados['ddd_3'] = telefones[2].ddd if 2 < len(telefones) else None
        dados['telefone_1'] = telefones[0].telefone if 0 < len(telefones) else None
        dados['telefone_2'] = telefones[1].telefone if 1 < len(telefones) else None
        dados['telefone_3'] = telefones[2].telefone if 2 < len(telefones) else None

        responsaveis = Responsavel.objects.filter(paciente=paciente)
        dados['responsavel_1'] = responsaveis[0].nome if 0 < len(responsaveis) else None
        dados['responsavel_2'] = responsaveis[1].nome if 1 < len(responsaveis) else None
        dados['responsavel_3'] = responsaveis[2].nome if 2 < len(responsaveis) else None

        form = FormPaciente(instance=paciente, initial=dados)

    return render(request, 'pacientes/edicao_paciente.html', {
        'form': form, 'paciente': paciente
    })


@login_required
def perfil_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    auxilios_entregues = Auxilio.objects.filter(paciente_id=pk)

    data_inicio = datetime.today() - relativedelta(months=1)
    # Maior data, caso o paciente tenha sido cadastrado recentemente
    data_inicio = data_inicio.date()
    data_inicio = max(data_inicio, paciente.data_cadastro)

    consultas = {}
    # Consultas
    consultas['registros'] = Consulta.objects.filter(paciente_id=pk).order_by('-data')
    consultas['contador'] = Consulta.objects.filter(paciente_id=pk).values('tipo__nome').annotate(quantidade=Count('paciente'))

    exames = Exame.objects.filter(paciente_id=pk)
    telefones = Telefone.objects.filter(paciente_id=pk)
    responsaveis = Responsavel.objects.filter(paciente_id=pk)
    status = paciente.ativo

    # Linha do tempo
    linha_do_tempo = gerar_linha_do_tempo(pk)

    # Logica ativar/desativar
    if request.method == 'POST':
        paciente.ativo = not paciente.ativo
        paciente.save()

    return render(request, 'pacientes/perfil_paciente.html', {
        'paciente': paciente, 'status': status, 'data_inicio': data_inicio,
        'consultas': consultas, 'telefones': telefones, 'responsaveis': responsaveis,
        'exames': exames, 'linha_do_tempo': linha_do_tempo
    })


@assistente_social_required
@login_required
def remover_foto(request, pk):
    info = {}
    if request.method == 'GET':
        paciente = get_object_or_404(Paciente, pk=pk)
        try:
            paciente.foto.delete(save=True)
            info['status'] = True
        except e:
            info['status'] = False
    return JsonResponse(info)
