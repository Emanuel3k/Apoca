# Descrição Inicial do Sistema V1.0

Este documento tem por finalidade descrever **o que** o sistema a ser desenvolvido deve fazer, baseado no primeiro levantamento de requisitos.

## Atores

Os seguintes atores deverão estar presentes no software:  

- **Assistente Social** - Profissional responsável por promover o bem-estar físico, psicológico e social | Terá acesso a todo sistema;
- **Médico** - Profissional da saúde autorizado pelo Estado para exercer a Medicina | Terá acesso a todo sistema;
- **Nutricionista** - Profissional de saúde que desenvolve ações no âmbito da atenção dietética e/ou segurança alimentar, destinadas tanto a um indivíduo como a um grupo populacional | Terá acesso restringido no sistema.

## Funções de cada Ator

- **Assistente Social**:
  - Cadastro e alteração de pacientes;
  - Gerenciamento de medicamentos, suplemtentos, materiais, equipamentos... (CRUD);
  - Controle de agendamentos;
  - Emissão de relatórios;
  - Cadastro de exames;
  - Acompanhamento de informações geradas em todo software;
  - Gerenciamento de auxílios (Materiais de Convalescença, Medicamentos, Complementos Alimentares, Cestas Básicas...).

- **Medico**:
  - Realizar consultas médicas;
  - Receitar medicamentos;
  - Emissão de chamados para compra de novos medicamentos; __remover__
  - Agendar consultas médicas;  __definir ainda__
  - Acompanhamento evolucional dos pacientes;
  - Encaminhar para exames;
  - Cadastro de exames.

- **Nutricionista**:
  - Realizar consultas nutricionais;
  - Cadastro de dados e informações nutricionais;
  - Emissão de chamados para compra de suplementos/complementos;
  - Receitar Complementos Alimentares e Suplementos;
  - Agendar consultas nutricionais;
  - Cadastro de exames.

## Outras funcionalidades para o sistema

- Permitir buscar as informações do paciente através de um código gerado no cadastro do mesmo;
- Emissão de relatório a ser assinado após receber algum auxílio;
- Expressar através tabelas e gráficos informações relevantes e úteis.
