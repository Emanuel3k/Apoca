from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def equipe(request):
    return render(request, 'pacientes/equipe_desenvolvimento.html')
