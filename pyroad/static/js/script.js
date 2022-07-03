function curvaCircularSimples() {
    let ac = document.getElementById('ac').value
    let pi = document.getElementById('pi').value
    let raio = document.getElementById('raio').value
    let velocidadeProjeto = document.getElementById('velocidade-projeto').value
    let emax = document.getElementById('e-max').value

    let formData = {
        "AC": parseFloat(ac),
        "PI": parseFloat(pi),
        "Raio": parseFloat(raio),
        "Vp": parseFloat(velocidadeProjeto),
        "e_max": parseFloat(emax)
    }
    $.ajax({
        url: "http://localhost:5000/curva-circular-simples",
        type: 'POST',
        data: JSON.stringify(formData),
        dataType: "json",
        contentType: "application/json",
    })
        .done(function (msg) {
            console.log('Requisição feita com sucesso!')

            criaTabela(msg.tabela)
            console.log('Tabela gerada com sucesso!')
        })
        .fail(function (jqXHR, textStatus, msg) {
            console.log('Requisição falhou!')
        });
}

function criaTabela(dadosTabela) {
    let divTabela = document.getElementById('table');
    divTabela.innerHTML = dadosTabela

    let tabela = document.getElementsByClassName('dataframe')[0]
    tabela.classList.add('table')
    tabela.classList.add('table-dark')

    divTabela.innerHTML += '<button class="btn btn-primary">DONWLOAD PDF</button>'
}


function outrafuncao(){

}

