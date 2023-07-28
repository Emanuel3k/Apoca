'use strict';

function exibe_inputs() {
    let option = $('#id_tipo>option:selected').text().toUpperCase();
    if (option == "MEDICAMENTO") {  // Medicamento
        $('#div_id_suplemento_alimentar').hide();
        $('#div_id_equipamento').hide();
        $('#div_id_medicamento').show();
    }
    else if (option == "EMPRÉSTIMO DE EQUIPAMENTO") {  // Emprestimo de equipamento
        $('#div_id_suplemento_alimentar').hide();
        $('#div_id_medicamento').hide();
        $('#div_id_equipamento').show();
    }
    else if (option == "SUPLEMENTO ALIMENTAR") {  // Suplemento alimentar
        $('#div_id_medicamento').hide();
        $('#div_id_equipamento').hide();
        $('#div_id_suplemento_alimentar').show();
    }
    else {
        $('#div_id_equipamento, #div_id_medicamento, #div_id_suplemento_alimentar').hide();
    }
}

$(document).ready(function() {
    // Logica inputs
    exibe_inputs();
    $('#id_tipo').change(function() {
        exibe_inputs();
    });

    flatpickr("#id_data_retirada", {
        dateFormat: "d/m/Y",
        locale: "pt",
        defaultDate: "today"
    });
    flatpickr("#id_hora_retirada", {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        time_24hr: true
    });
});
