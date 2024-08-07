from django import forms
from .models import Conta
from decimal import *

class ContaForms(forms.ModelForm):
    """
    Formulário para criação e edição de contas.
    """

    class Meta:
        model = Conta
        exclude = ['saldo_atual', 'data_criacao', 'usuario', 'limite_atual']
        labels = {
            'nome': 'Nome',
            'descricao': 'Descrição',
            'saldo_inicial': 'Saldo Inicial',
            'limite': 'Limite total de crédito',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Nubank'},),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite uma descrição'},),
            'saldo_inicial': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0,00'}),
            'limite': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0,00'}),
        }

    def clean_saldo_inicial(self):
        """
        Valida o valor do saldo inicial.
        """
        saldo_inicial = self.cleaned_data['saldo_inicial']
        
        if isinstance(saldo_inicial, str):
            saldo_inicial = saldo_inicial.replace(',', '.')

        try:
            saldo_inicial = Decimal(saldo_inicial)
        except ValueError:
            raise forms.ValidationError('Saldo inicial inválido.')

        if saldo_inicial < 0:
            raise forms.ValidationError('Saldo inicial não pode ser negativo.')

        return saldo_inicial
    
    def clean_limite(self):
        """
        Valida o valor do limite de crédito.
        """
        limite = self.cleaned_data['limite']
        
        if isinstance(limite, str):
            limite = limite.replace(',', '.')

        try:
            limite = Decimal(limite)
        except ValueError:
            raise forms.ValidationError('Limite de crédito inválido.')

        if limite < 0:
            raise forms.ValidationError('Limite de crédito não pode ser negativo.')

        return limite