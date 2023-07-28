$(document).ready(function() {
    $('input').keydown(function (e) {
        if (e.keyCode == 13) {
            event.preventDefault();
        }
    });

    $('#limpar-foto').click(function(event) {
        event.preventDefault();
        $('#foto-cadastro').attr('src', '/static/assets/images/users/user-img.png');
        // remover
        var url = $('#url_remover_foto').val();
        $.get(url, function(data) {
            if (data.status) {
                $('#modal_confirmacao').modal();
            }
        });
    });

    flatpickr("#id_data_cadastro", {
        dateFormat: "d/m/Y",
        locale: "pt",
    });

    flatpickr("#id_data_nascimento", {
        dateFormat: "d/m/Y",
        locale: "pt",
        allowInput: true
    });

    var renda = $('#id_renda_familiar')[0];
    var valor_formatado = new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(Number(renda.value));
    renda.value = valor_formatado.substring(3);
});

function lerURL(input) {
    if (input.files && input.files[0]) {

        var leitor = new FileReader();

        leitor.onload = function (e) {
            $('#foto-cadastro')
                .attr('src', e.target.result)
                .width(200)
                .height(200)
                .css('border-radius', '400px');
        };

        leitor.readAsDataURL(input.files[0]);
    }
}
