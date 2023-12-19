from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q, Count

from ..models import *

from datetime import datetime
from dateutil.relativedelta import relativedelta


@login_required
def inicio(request):
    pacientes = Paciente.objects.all().order_by('-id')[:7]
    atv_diaria = consulta_atividades_diarias()
    cidades = Cidade.objects.all()
    data_inicio = datetime.today() - relativedelta(months=1)
    racas = consulta_racas()

    # lista de equipamentos empresados a mais de 60 dias
    equipamentosAuxilio = Auxilio.objects.select_related('equipamento').filter(
        tipo__abreviacao='EE',
        data_retirada__lte=(datetime.today() - relativedelta(days=60)),
        equipamento__emprestado=True,
        data_devolucao__isnull=True,
    ).order_by('data_retirada')

    equipamentosAuxilio = equipamentosAuxilio.all()

    return render(request, 'pacientes/index.html', {
        'pacientes': pacientes, 'atv_diaria': atv_diaria, 'cidades': cidades,
        'data_inicio': data_inicio, 'racas': racas, 'equipamentosAuxilio': equipamentosAuxilio
    })


def consulta_atividades_diarias():
    atv_diaria = {}
    atv_diaria['pacientes'] = Paciente.objects.filter(data_cadastro=datetime.today()).count()
    atv_diaria['auxilios'] = Auxilio.objects.filter(data_retirada=datetime.today()).count()
    atv_diaria['consultas'] = Consulta.objects.filter(data=datetime.today()).count()
    atv_diaria['exames'] = Exame.objects.filter(data=datetime.today()).count()

    return atv_diaria


def consulta_racas():
    racas = (
        Paciente.objects.filter(raca='Branca').count(),
        Paciente.objects.filter(raca='Preta').count(),
        Paciente.objects.filter(raca='Parda').count(),
        Paciente.objects.filter(raca='Amarela').count(),
        Paciente.objects.filter(raca='Indígena').count(),
        Paciente.objects.filter(raca='Não informado').count()
    )

    return racas


@login_required
def filtrar_info_gerais(request):

    if request.method == 'GET':
        data_inicio = request.GET.get('data_inicio')
        data_inicio = datetime.strptime(data_inicio, '%d/%m/%Y').date()
        data_fim = request.GET.get('data_fim')
        data_fim = datetime.strptime(data_fim, '%d/%m/%Y').date()
        cidade = request.GET.get('cidade')

        pacientes = {}
        consulta_exame = {}

        if cidade == 'Total':
            pacientes['ativos'] = Paciente.objects.filter(ativo=True).count()
            pacientes['inativos'] = Paciente.objects.filter(ativo=False).count()
            pacientes['total'] = Paciente.objects.all().count()

            filtro_auxilio = Count('auxilio', filter=Q(auxilio__data_retirada__gte=data_inicio) &
                Q(auxilio__data_retirada__lte=data_fim)
            )
            tipo_auxilios = TipoAuxilio.objects.all().values('nome').annotate(quantidade=filtro_auxilio)
            tipo_auxilios = list(tipo_auxilios)

            # Gerenado dados sobre consultas e exames
            consulta_exame['consulta'] = Consulta.objects.filter(
                data__gte=data_inicio,
                data__lte=data_fim
            ).count()
            consulta_exame['exame'] = Exame.objects.filter(
                data__gte=data_inicio,
                data__lte=data_fim
            ).count()
        else:
            # Gerando dados sobre os pacientes ativos, inativos e total
            pacientes['ativos'] = Paciente.objects.filter(ativo=True, cidade__nome=cidade).count()
            pacientes['inativos'] = Paciente.objects.filter(ativo=False, cidade__nome=cidade).count()
            pacientes['total'] = Paciente.objects.filter(cidade__nome=cidade).count()

            filtro_auxilio = Count('auxilio', filter=Q(auxilio__paciente__cidade__nome=cidade) &
                Q(auxilio__data_retirada__gte=data_inicio) &
                Q(auxilio__data_retirada__lte=data_fim)
            )
            tipo_auxilios = TipoAuxilio.objects.all().values('nome').annotate(quantidade=filtro_auxilio)
            tipo_auxilios = list(tipo_auxilios)

            # Gerenado dados sobre consultas e exames
            consulta_exame['consulta'] = Consulta.objects.filter(
                paciente__cidade__nome=cidade,
                data__gte=data_inicio,
                data__lte=data_fim
            ).count()
            consulta_exame['exame'] = Exame.objects.filter(
                paciente__cidade__nome=cidade,
                data__gte=data_inicio,
                data__lte=data_fim
            ).count()

        data = {'pacientes': pacientes, 'tipo_auxilios': tipo_auxilios, 'consulta_exame': consulta_exame}

    return JsonResponse(data, safe=False)
