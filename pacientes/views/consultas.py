from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from ..decorators import *
from ..models import Consulta, Paciente
from ..forms import FormConsulta


@assistente_social_required
@login_required
def consultas(request):
    consultas = Consulta.objects.all().order_by('-data')

    return render(request, 'consulta/consulta.html', {'consultas': consultas})


@assistente_social_required
@login_required
def cadastrar_consulta(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    form = FormConsulta(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.paciente = paciente
            consulta.save()

            messages.success(request, 'Consulta cadastrada com sucesso.')
            return redirect('pacientes:perfil_paciente', pk=consulta.paciente.pk)

        messages.error(request, 'Não foi possível cadastrar a consulta.')
    return render(request, 'consulta/cadastro_consulta.html', {'form': form, 'paciente': paciente})


@assistente_social_required
@login_required
def editar_consulta(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)

    if request.method == 'POST':
        form = FormConsulta(request.POST, instance=consulta)
        if form.is_valid():
                form.save()
                messages.success(request, 'Consulta editada com sucesso!')
                return redirect('pacientes:perfil_paciente', pk=consulta.paciente.id)

        messages.error(request, 'Não foi possível editar a consulta.')
    else:
        form = FormConsulta(instance=consulta)

    return render(request, 'consulta/edicao_consulta.html', {'form': form, 'paciente': consulta.paciente})
