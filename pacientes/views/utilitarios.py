from django.shortcuts import get_object_or_404
from django.contrib import messages

from ..models import *


def cadastrar_telefone(ddd, telefone, paciente):
    regras = [
        telefone,
        not telefone.isspace(),
        ddd,
        not ddd.isspace()
    ]
    if all(regras):
        Telefone.objects.create(
            paciente=paciente,
            ddd=ddd,
            telefone=telefone
        )


def editar_telefones(telefones, paciente):
    tels = Telefone.objects.filter(paciente=paciente).order_by('pk')

    for n in range(min(len(tels), 3)):
        regras = [
            telefones[n]['ddd'],
            not telefones[n]['ddd'].isspace(),
            telefones[n]['telefone'],
            not telefones[n]['telefone'].isspace(),
        ]
        if all(regras):
            tels[n].ddd = telefones[n].get('ddd')
            tels[n].telefone = telefones[n].get('telefone')
            tels[n].save()
        else:  # Apaga do banco se remover na interface
            tels[n].delete()

    # remove da lista
    telefones = telefones[len(tels):]
    # Telefones que não estao no banco precisam ser criados
    for tel in telefones:
        cadastrar_telefone(tel['ddd'], tel['telefone'], paciente)


def cadastrar_responsavel(responsavel, paciente):
    if responsavel and not responsavel.isspace():
        Responsavel.objects.create(
            paciente=paciente,
            nome=responsavel
        )


def editar_responsaveis(responsaveis, paciente):
    resps = Responsavel.objects.filter(paciente=paciente).order_by('pk')

    for n in range(min(len(resps), 3)):
        regras = [
            responsaveis[n],
            not responsaveis[n].isspace()
        ]
        if all(regras):
            resps[n].nome = responsaveis[n]
            resps[n].save()
        else:  # Apaga do banco se remover na interface
            resps[n].delete()

    # remove da lista
    responsaveis = responsaveis[len(resps):]
    # responsaveis que não estao no banco precisam ser criados
    for resp in responsaveis:
        cadastrar_responsavel(resp, paciente)


def formatar_cpf(cpf_desformatado):
    cpf = cpf_desformatado[:3]
    cpf += '.' + cpf_desformatado[3:6]
    cpf += '.' + cpf_desformatado[6:9]
    cpf += '-' + cpf_desformatado[9:]

    return cpf


def desformatar_cpf(cpf_formatado):
    return cpf_formatado.replace('.', '').replace('-', '')


def formatar_cep(cep_desformatado):
    cep = cep_desformatado[:4]
    cep += '-' + cep_desformatado[5:]

    return cep


def desformatar_cep(cep_formatado):
    return cep_formatado.replace('-', '')


