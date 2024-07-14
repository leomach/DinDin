document.getElementById('field-categoria').addEventListener('change', (e) => {
    var select = document.getElementById("field-categoria");
    let value = select.options[select.selectedIndex].value;
    var subcategoriaSelect = document.getElementById('field-subcategoria');
    
    subcategoriaSelect.innerHTML = '<option value="">Carregando subcategorias...</option>';
    fetch('/get_subcategorias/' + value + '/')
        .then(response => response.json())
        .then(data => {
            subcategoriaSelect.innerHTML = '<option value="">Selecione uma subcategoria</option>';
            data.forEach(function(subcategoria) {
                var option = document.createElement('option');
                option.value = subcategoria.id;
                option.textContent = subcategoria.nome;
                subcategoriaSelect.appendChild(option);
            });
        });
})