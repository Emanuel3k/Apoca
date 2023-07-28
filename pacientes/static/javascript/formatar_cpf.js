cpf = document.getElementById("id_cpf");
cpf.maxLength = 14;

cpf.addEventListener('keypress', function (){
    if (cpf.value.length == 3 || cpf.value.length == 7) {
        cpf.value += ".";
    } else if (cpf.value.length == 11) {
        cpf.value += "-";
    }
});
