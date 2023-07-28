$('#id_renda_familiar').keyup(function(e) {
    var valor = e.target.value;
    
    if(valor == ''){ 
        e.target.value = '';
        return;
    }

    valor = valor + '';
    valor = parseInt(valor.replace(/[\D]+/g,''));
    valor = valor + '';
    valor = valor.replace(/([0-9]{2})$/g, ",$1");
  
    if (valor.length > 6) {
      valor = valor.replace(/([0-9]{3}),([0-9]{2}$)/g, ".$1,$2");
    }
    
    e.target.value = valor;
});