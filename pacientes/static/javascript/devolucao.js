$(document).ready(function() {
    flatpickr("#id_data_devolucao", {
        dateFormat: "d/m/Y",
        locale: "pt",
        // TODO defaultDate: "today"
    });
    flatpickr("#id_hora_devolucao", {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        time_24hr: true
    });
});