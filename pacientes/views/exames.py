from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from ..decorators import *
from ..models import Exame, Paciente
from ..forms import FormExame


@assistente_social_required
@login_required
def exames(request):
    exames = Exame.objects.all().order_by('-data')

    return render(request, 'exame/exame.html', {'exames': exames})


@assistente_social_required
@login_required
def cadastrar_exame(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    form = FormExame(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            exame = form.save(commit=False)
            exame.paciente = paciente
            exame.save()

            messages.success(request, 'Exame cadastrado com sucesso.')
            return redirect('pacientes:perfil_paciente', pk=exame.paciente.pk)

        messages.error(request, 'Não foi possível cadastrar o exame.')
    return render(request, 'exame/cadastro_exame.html', {'form': form, 'paciente': paciente})


@assistente_social_required
@login_required
def editar_exame(request, pk):
    exame = get_object_or_404(Exame, pk=pk)

    if request.method == 'POST':
        form = FormExame(request.POST, instance=exame)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exame editado com sucesso!')
            return redirect('pacientes:perfil_paciente', pk=exame.paciente.id)

        messages.error(request, 'Não foi possível editar o exame.')
    else:
        form = FormExame(instance=exame)

    return render(request, 'exame/edicao_exame.html', {'form': form, 'paciente': exame.paciente})
