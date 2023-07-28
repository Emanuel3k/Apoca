from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Count

from ..models import *

from datetime import datetime


@login_required
def filtrar_auxilios(request, pk):

    if request.method == 'GET':
        paciente = get_object_or_404(Paciente, pk=pk)
        data_inicio = request.GET.get('data_inicio')
        data_inicio = datetime.strptime(data_inicio, '%d/%m/%Y').date()
        data_fim = request.GET.get('data_fim')
        data_fim = datetime.strptime(data_fim, '%d/%m/%Y').date()

        filtro_auxilio = Count('auxilio', filter=Q(auxilio__paciente=paciente) &
            Q(auxilio__data_retirada__gte=data_inicio) &
            Q(auxilio__data_retirada__lte=data_fim)
        )
        tipo_auxilios = TipoAuxilio.objects.all().values('nome').annotate(quantidade=filtro_auxilio)
        tipo_auxilios = list(tipo_auxilios)

    return JsonResponse(tipo_auxilios, safe=False)


def gerar_linha_do_tempo(pk):
    auxilios = Auxilio.objects.filter(paciente_id=pk)
    consultas = Consulta.objects.filter(paciente_id=pk)
    exames = Exame.objects.filter(paciente_id=pk)

    lista_eventos = normalizar_eventos(auxilios) + normalizar_eventos(consultas) + normalizar_eventos(exames)
    # Ordenacao
    lista_eventos = sorted(lista_eventos, key=lambda evento: evento['data'], reverse=True)

    return lista_eventos


def normalizar_eventos(lista_eventos):
    eventos = []
    for e in lista_eventos:
        evento = {}
        evento['grupo'] = type(e).__name__
        evento['objeto'] = e
        if isinstance(e, Auxilio):
            evento['data'] = e.data_retirada
            evento['horario'] = e.hora_retirada
            evento['tipo'] = e.tipo.nome
            evento['quantidade'] = e.quantidade

            if evento['tipo'] == 'Medicamento':
                evento['nome'] = e.medicamento.nome
            elif evento['tipo'] == 'Empréstimo de equipamento':
                evento['nome'] = e.equipamento.nome
                evento['etiqueta'] = e.equipamento.etiqueta
                if e.data_devolucao:
                    evento['data_devolucao'] = e.data_devolucao
                    evento['hora_devolucao'] = e.hora_devolucao
        elif isinstance(e, Consulta):
            evento['tipo'] = ('Consulta {}' .format(e.tipo))
            evento['data'] = e.data
            evento['observacao'] = e.observacao
        elif isinstance(e, Exame):
            evento['tipo'] = e.tipo
            evento['data'] = e.data
        eventos.append(evento.copy())

    return eventos
