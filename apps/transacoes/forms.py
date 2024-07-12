from django import forms
from .models import Transacao, TransacaoParcelada, Parcela
from ..conta.models import Conta
from ..subcategorias.models import Subcategoria, Categoria

class TransacaoParceladaForm(forms.ModelForm):
    """Formulário para transações parceladas."""

    class Meta:
        model = TransacaoParcelada
        fields = [
            'data',
            'descricao',
            'parcelas',
            'valor_total',
            'conta',
            'categoria',
            'subcategoria',
        ]
        exclude = ['id', 'usuario']
        labels = {
            'data': 'Data da transação',
            'descricao': 'Descrição',
            'parcelas': 'Quantidade de parcelas',
            'valor_total': 'Valor total da transação',
            'conta': 'Conta',
            'categoria': 'Categoria',
            'subcategoria': 'Subcategoria',
        }
        widgets = {
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'parcelas': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'conta': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control', 'id': 'field-categoria'}),
            'subcategoria': forms.Select(attrs={'class': 'form-control', 'id': 'field-subcategoria'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['conta'].queryset = Conta.objects.filter(usuario=user)
            self.fields['categoria'].queryset = Categoria.objects.filter(usuario=user)
            self.fields['subcategoria'].queryset = Subcategoria.objects.filter(usuario=user)

    def clean_valor(self):
        """
        Valida o campo 'valor'.
        """
        valor = self.cleaned_data['valor_total']

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
            'conta': forms.Select(attrs={'class': 'form-control'},),
            'categoria': forms.Select(attrs={'class': 'form-control', 'id': 'field-categoria'}),
            'subcategoria': forms.Select(attrs={'class': 'form-control', 'id': 'field-subcategoria'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['conta'].queryset = Conta.objects.filter(usuario=user)
            self.fields['categoria'].queryset = Categoria.objects.filter(usuario=user)
            self.fields['subcategoria'].queryset = Subcategoria.objects.filter(usuario=user)
        

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
    
class ParcelaForm(forms.ModelForm):
    """Formulário para parcelas de transações."""
    class Meta:
        model = Parcela
        fields = [
            'data',
            'valor_parcela'
        ]
        exclude = ['id', 'transacao_parcelada', 'usuario', 'numero_parcela', 'status']
        labels = {
            'data': 'Data da parcela',
            'valor_parcela': 'Valor da parcela',
        }
        widgets = {
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor_parcela': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_valor_parcela(self):
        """
        Valida o campo 'valor_parcela'.
        """
        valor_parcela = self.cleaned_data['valor_parcela']

        if valor_parcela <= 0:
            raise forms.ValidationError('O valor da parcela deve ser maior que zero.')

        return valor_parcela
        
