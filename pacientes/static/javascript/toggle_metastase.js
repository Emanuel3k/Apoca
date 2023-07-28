$('#id_metastase').click(function(e) {
    $('.descricao_metastase').toggleClass('d-none');
});

// Função para mostrar localização da metástase
// caso o campo estaja "Metástase" esteja ativo.
$(document).ready(function() {
    if ($('#id_metastase').attr('checked')) {
        $('.descricao_metastase').removeClass('d-none');
    }
});