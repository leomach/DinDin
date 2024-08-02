from django import forms
from .models import Categoria

class CategoriaForm(forms.ModelForm):
    """
    Formulário para criação e edição de categorias.
    """

    class Meta:
        model = Categoria
        fields = ['nome', 'descricao', 'tipo']
        exclude = ['saldo_atual', 'data_criacao', 'usuario']  # Exclua esses campos se necessário
        labels = {
            'nome': 'Nome',
            'descricao': 'Descrição',
            'tipo': 'Receitas ou despesas?'
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Salário', 'required': True}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional'}),
            'tipo': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Receita/Despesa'})
        }

    def clean_nome(self):
        """
        Valida o campo 'nome'.
        """
        nome = self.cleaned_data['nome']

        if not nome.strip():
            raise forms.ValidationError('O nome da categoria não pode ser vazio.')

        return nome
