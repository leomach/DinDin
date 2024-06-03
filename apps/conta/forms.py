from django import forms
from .models import Conta

class ContaForms(forms.ModelForm):
    """
    Formulário para criação e edição de contas.
    """

    class Meta:
        model = Conta
        exclude = ['saldo_atual', 'data_criacao', 'usuario',]
        labels = {
            'nome': 'Nome',
            'descricao': 'Descrição',
            'saldo_atual': 'Saldo Atual',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Nubank'},),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite uma descrição'},),
            'saldo_inicial': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
        }

    def clean_saldo_inicial(self):
        """
        Valida o valor do saldo inicial.
        """
        saldo_inicial = self.cleaned_data['saldo_inicial']

        try:
            saldo_inicial = float(saldo_inicial)
        except ValueError:
            raise forms.ValidationError('Saldo inicial inválido.')

        if saldo_inicial < 0:
            raise forms.ValidationError('Saldo inicial não pode ser negativo.')

        return saldo_inicial