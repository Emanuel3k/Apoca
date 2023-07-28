'use strict';

function atualizar_auxilios() {
    let url = $('#url_filtrar_auxilios').val();

    let datas = {
        data_inicio: $('#data-inicio').val(),
        data_fim: $('#data-fim').val()
    }

    $.get(url, datas, function(tipo_auxilios) {
        let texto = '';
        let total = 0;

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
        $('#tipo_auxilios_user').html(texto);
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
    $('#data-inicio, #data-fim').change(atualizar_auxilios);

    $('#tabela-consultas').DataTable(
        {
            language: {
                search: "Pesquisa:",
                searchPlaceholder: "Procure por uma consulta",
                info: "Mostrando _START_ até _END_ de _TOTAL_ registros",
                infoEmpty: "Mostrando 0 até 0 de 0 registros",
                infoFiltered: "(filtrado do total de _MAX_ registros)",
                emptyTable: "Nenhuma consulta registrada",
                zeroRecords: "Nenhum resultado encontrado",
                processing: "Processando...",
                loadingRecords: "Carregando...",
                lengthMenu: "Mostrar _MENU_ registros",
                paginate: {
                    first: "Primeiro",
                    last: "Último",
                    next: "<i class=\"mdi mdi-chevron-right\">",
                    previous: "<i class=\"mdi mdi-chevron-left\">"
                }
            }
        }
    );

    // Retirando classes do limitador e do filtro
    $('#tabela-consultas_length').children().children().removeClass('custom-select-sm');
    $('#tabela-consultas_length').children().children().removeClass('form-control-sm');
    $('#tabela-consultas_filter').children().children().removeClass('form-control-sm');
});
