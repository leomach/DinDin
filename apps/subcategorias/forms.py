from django import forms
from .models import Subcategoria, Categoria

class SubcategoriaForm(forms.ModelForm):
    """
    Formulário para criação e edição de subcategorias.
    """

    class Meta:
        model = Subcategoria
        fields = ['nome', 'descricao', 'categoria']
        exclude = ['usuario']  # Exclua este campo se necessário
        labels = {
            'nome': 'Nome',
            'descricao': 'Descrição',
            'categoria': 'Categoria',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Salário da empresa', 'required': True}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, request, *args, **kwargs):
        """
        Construtor do formulário para receber o objeto request.
        """
        super().__init__(*args, **kwargs)
        self.request = request
        self.set_categoria_choices()

    def set_categoria_choices(self):
        """
        Define as opções de categoria filtradas por usuário.
        """
        if self.request:
            self.fields['categoria'].choices = [(categoria.pk, categoria.nome) for categoria in Categoria.objects.filter(usuario=self.request.user)]

    def clean_nome(self):
        """
        Valida o campo 'nome'.
        """
        nome = self.cleaned_data['nome']

        if not nome.strip():
            raise forms.ValidationError('O nome da subcategoria não pode ser vazio.')

        return nome
