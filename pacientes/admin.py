from django.contrib import admin

from .models import *

admin.site.register(Paciente)
admin.site.register(Doenca)
admin.site.register(Cidade)
admin.site.register(Telefone)
admin.site.register(Equipamento)
admin.site.register(Medicamento)
admin.site.register(TipoAuxilio)
admin.site.register(Auxilio)
admin.site.register(Responsavel)
admin.site.register(TipoConsulta)
admin.site.register(Consulta)
admin.site.register(Exame)
