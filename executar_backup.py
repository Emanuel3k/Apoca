#!/usr/bin/env python3

from apoca import settings

# from multiprocessing import Process
import os
import datetime
import time
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


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
        print("ERRO: Nao foi possivel carregar as credenciais")

    drive = GoogleDrive(gauth)
    # Upload arquivo
    file = drive.CreateFile({'parents': [{'id': '1Fd1xTGtZAN4PwUgzLxjYeJmrKJmjc2nd'}]})
    file.SetContentFile(arquivo)
    file['title'] = nome
    file.Upload()
    # Remove arquivo local
    time.sleep(5)
    os.remove(arquivo)


# Se executado como script
if __name__ == '__main__':
    criar_backup()
