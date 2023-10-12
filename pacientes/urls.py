from django.urls import path
from . import views

app_name = 'pacientes'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('pacientes/', views.pacientes, name='pacientes'),
    path('paciente/cadastrar/', views.cadastrar_paciente, name='cadastrar_paciente'),
    path('paciente/<int:pk>/editar/', views.editar_paciente, name='editar_paciente'),
    path('paciente/<int:pk>/perfil_paciente', views.perfil_paciente, name='perfil_paciente'),
    path('paciente/<int:pk>/consultas/cadastrar/', views.cadastrar_consulta, name='cadastrar_consulta'),
    path('paciente/<int:pk>/consultas/editar/', views.editar_consulta, name='editar_consulta'),
    path('paciente/<int:pk>/exames/cadastrar/', views.cadastrar_exame, name='cadastrar_exame'),
    path('paciente/<int:pk>/exames/editar/', views.editar_exame, name='editar_exame'),
    path('paciente/<int:pk>/auxilio/cadastrar/', views.cadastrar_auxilio, name='cadastrar_auxilio'),
    path('paciente/<int:pk>/auxilio/editar/', views.editar_auxilio, name='editar_auxilio'),

    path('auxilios/', views.listar_auxilios, name='listar_auxilios'),
    path('auxilios/equipamentos_emprestados', views.listar_equipamentos_emprestados, name='listar_equipamentos_emprestados'),
    path('auxilios/<int:pk>/registrar_devolucao', views.registrar_devolucao, name='registrar_devolucao'),
    path('auxilios/<int:pk>/renovar_emprestimo', views.renovar_emprestimo, name='renovar_emprestimo'),
    path('auxilios/<int:pk>/detalhes_auxilio', views.detalhes_auxilio, name='detalhes_auxilio'),

    # URLS ajax
    path('paciente/<int:pk>/remover_foto', views.remover_foto, name='remover_foto'),
    path('paciente/<int:pk>/filtrar_auxilios', views.filtrar_auxilios, name='filtrar_auxilios'),
    path('filtrar_info_gerais/', views.filtrar_info_gerais, name='filtrar_info_gerais'),

    # URL administrativo
    path('administrativo/', views.administrativo, name='administrativo'),
    path('administrativo/backup/', views.backup, name='backup'),

    # URL apresentação equipe
    path('equipe/', views.equipe, name='equipe'),

    # Cadastros gerais
    path('cadastros-gerais/medicamento/', views.medicamentos, name='medicamentos'),
    path('cadastros-gerais/medicamento/cadastrar/', views.cadastrar_medicamento, name='cadastrar_medicamento'),
    path('cadastros-gerais/medicamento/<int:pk>/editar/', views.editar_medicamento, name='editar_medicamento'),
    path('cadastros-gerais/equipamento/', views.equipamentos, name='equipamentos'),
    path('cadastros-gerais/equipamento/cadastrar/', views.cadastrar_equipamento, name='cadastrar_equipamento'),
    path('cadastros-gerais/equipamento/<int:pk>/editar/', views.editar_equipamento, name='editar_equipamento'),
    path('cadastros-gerais/tipo-auxilio/', views.tipos_auxilios, name='tipos_auxilios'),
    path('cadastros-gerais/tipo-auxilio/cadastrar/', views.cadastrar_tipo_auxilio, name='cadastrar_tipo_auxilio'),
    path('cadastros-gerais/tipo-auxilio/<int:pk>/editar/', views.editar_tipo_auxilio, name='editar_tipo_auxilio'),
    path('cadastros-gerais/cidade/', views.cidades, name='cidades'),
    path('cadastros-gerais/cidade/cadastrar/', views.cadastrar_cidade, name='cadastrar_cidade'),
    path('cadastros-gerais/cidade/<int:pk>/editar/', views.editar_cidade, name='editar_cidade'),
    path('cadastros-gerais/tipo-consulta/', views.tipos_consulta, name='tipos_consulta'),
    path('cadastros-gerais/tipo-consulta/cadastrar/', views.cadastrar_tipo_consulta, name='cadastrar_tipo_consulta'),
    path('cadastros-gerais/tipo-consulta/<int:pk>/editar/', views.editar_tipo_consulta, name='editar_tipo_consulta'),
    path('cadastros-gerais/doenca/', views.doencas, name='doencas'),
    path('cadastros-gerais/doenca/cadastrar/', views.cadastrar_doenca, name='cadastrar_doenca'),
    path('cadastros-gerais/doenca/<int:pk>/editar/', views.editar_doenca, name='editar_doenca'),
    path('cadastros-gerais/suplemento-alimentar/', views.sup_alimentares, name='sup_alimentares'),
    path('cadastros-gerais/suplemento-alimentar/cadastrar/', views.cadastrar_sup_alimentar, name='cadastrar_sup_alimentar'),
    path('cadastros-gerais/suplemento-alimentar/<int:pk>/editar/', views.editar_sup_alimentar, name='editar_sup_alimentar'),

    # Consulta
    path('consultas/', views.consultas, name='consultas'),

    # Exame
    path('exames/', views.exames, name='exames'),
]
