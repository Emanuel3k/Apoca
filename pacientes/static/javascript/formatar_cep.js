cep = document.getElementById("id_cep");

cep.addEventListener('keypress', function (){
    if (cep.value.length == 5) {
        cep.value += "-";
    }
});
