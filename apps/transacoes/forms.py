from django import forms
from .models import Transacao
from ..subcategorias.models import Subcategoria

class TransacaoForm(forms.ModelForm):
    """Formulário para transações."""

    class Meta:
        model = Transacao
        fields = [
            'data',
            'descricao',
            'valor',
            'tipo',
            'conta',
            'categoria',
            'subcategoria',
        ]
        exclude = ['id', 'usuario']
        labels = {
            'data': 'Data',
            'descricao': 'Descrição',
            'valor': 'Valor',
            'tipo': 'Tipo',
            'conta': 'Conta',
            'categoria': 'Categoria',
            'subcategoria': 'Subcategoria',
        }
        widgets = {
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'conta': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control', 'id': 'field-categoria'}),
            'subcategoria': forms.Select(attrs={'class': 'form-control', 'id': 'field-subcategoria'}),
        }

    def clean_valor(self):
        """
        Valida o campo 'valor'.
        """
        valor = self.cleaned_data['valor']

        if valor <= 0:
            raise forms.ValidationError('O valor da transação deve ser maior que zero.')

        return valor
    
    def clean_categoria(self):
        """
        Aplica filtro por categoria no campo 'subcategoria'.
        """
        categoria_selecionada = self.cleaned_data['categoria']
        subcategorias = Subcategoria.objects.filter(categoria=categoria_selecionada)

        # Atualizar o campo 'subcategoria' com as opções filtradas
        self.fields['subcategoria'].queryset = subcategorias
        return categoria_selecionada

