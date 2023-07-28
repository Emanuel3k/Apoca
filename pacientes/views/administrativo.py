from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from ..decorators import *
from multiprocessing import Process
import os
import datetime
import time
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


@assistente_social_required
@login_required
def administrativo(request):
    return render(request, 'administrativo/administrativo.html')


@assistente_social_required
@login_required
def backup(request):
    try:
        p = Process(target=criar_backup)
        p.start()
    except Exception:
        messages.error(request, 'Erro ao realizar backup. Tente novamente em alguns instantes.')
    else:
        messages.success(request, 'O processo de backup foi agendado e será realizado assim que possível. Aguarde alguns instantes.')

    return redirect('pacientes:administrativo')


def criar_backup():
    dir = os.path.join(settings.BASE_DIR, 'backups/{}'.format(datetime.date.today().year))
    if not os.path.exists(dir):
        os.makedirs(dir)
    agora = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    nome = '{}-backup.sql.gz'.format(agora)
    arquivo = os.path.join(dir, nome)
    os.system(f'mysqldump -h {settings.DB_HOST} -u {settings.DB_USER} -p\'{settings.DB_PASSWORD}\' \'{settings.DB_NAME}\' | gzip -9 -c > {arquivo}')
    # Drive autenticacao
    gauth = GoogleAuth()
    try:
        gauth.LoadCredentialsFile('mycreds.txt')
    except Exception:
        pass
    else:
        gauth.LocalWebserverAuth()
        gauth.SaveCredentialsFile('mycreds.txt')

    drive = GoogleDrive(gauth)
    # Upload arquivo
    file = drive.CreateFile({'parents': [{'id': '1Fd1xTGtZAN4PwUgzLxjYeJmrKJmjc2nd'}]})
    file.SetContentFile(arquivo)
    file['title'] = nome
    file.Upload()
    # Remove arquivo local
    time.sleep(5)
    os.remove(arquivo)
