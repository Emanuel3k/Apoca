'use strict';

function atualizar_auxilios() {
    let url = $('#url-filtro').val();

    let data = {
        data_inicio: $('#data-inicio').val(),
        data_fim: $('#data-fim').val(),
        cidade: $('#cidade option:selected').text()
    }

    $.get(url, data, function(data) {
        let texto, total, pacientes, tipo_auxilios, consultas, exames;
        pacientes = data.pacientes;
        tipo_auxilios = data.tipo_auxilios;
        consultas = data.consulta_exame.consulta;
        exames = data.consulta_exame.exame;

        $('#paciente-ativo').text(pacientes.ativos);
        $('#paciente-inativo').text(pacientes.inativos);
        $('#paciente-total').text(pacientes.total);
        $('#consulta').text(consultas);
        $('#exame').text(exames);

        texto = '';
        total = 0;

        $.each(tipo_auxilios, function () {
            texto += `<div class="col-md-3 text-center">
                <div>
                    <p class="text-muted mb-2">${this.nome}</p>
                    <h5 class="mb-4">${this.quantidade}</h5>
                </div></div>`;
            total += this.quantidade;
        });

        texto += `<div class="col-md-3 text-center">
            <div>
                <p class="mb-2">Total</p>
                <h5 class="mb-4">${total}</h5>
            </div></div>`;
        $('#tipo_auxilios').html(texto);
    });
}

$(document).ready(function() {
    flatpickr("#data-inicio", {
        dateFormat: "d/m/Y",
        locale: "pt",
    });

    flatpickr("#data-fim", {
        dateFormat: "d/m/Y",
        locale: "pt",
        defaultDate: "today"
    });

    atualizar_auxilios();
    $('#data-inicio, #data-fim, #cidade').change(atualizar_auxilios);
});
