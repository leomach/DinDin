function timeToggle() {
    document.getElementById(`mensal`).classList.toggle("none");
    document.getElementById(`anual`).classList.toggle("none");
    document.getElementById(`gerais_mes`).classList.toggle("none");
    document.getElementById(`gerais_ano`).classList.toggle("none");
    
    document.getElementById(`blocos_mes`).classList.toggle("none");
    document.getElementById(`blocos_ano`).classList.toggle("none");
    document.getElementById(`blocos_mes`).classList.toggle("blocos");
    document.getElementById(`blocos_ano`).classList.toggle("blocos");
    
    document.getElementById(`transacoes_mes`).classList.toggle("none");
    document.getElementById(`transacoes_mes`).classList.toggle("transacoes-list");
}