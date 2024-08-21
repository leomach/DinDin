from django.db import models
from django.contrib.auth.models import User
from ..conta.models import Conta
from ..categorias.models import Categoria
from ..subcategorias.models import Subcategoria
import datetime

class TransacaoParcelada(models.Model):
    """
    Modelo para representar transações financeiras parceladas.
    """
    class Meta:
        db_table = 'tansacao_parcelada'
        verbose_name = 'TransacaoParcela'
        verbose_name_plural = 'TransacaoParceladas'

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE)
    data = models.DateField(default=datetime.date.today)
    descricao = models.CharField(max_length=255)
    parcelas = models.IntegerField(blank=False, null=False)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.descricao} - R${self.valor_total:.2f}'


        
class Parcela(models.Model):
    """
    Modelo para representar parcelas de transações financeiras.
    """
    class Meta:
        db_table = 'parcela'
        verbose_name = 'Parcela'
        verbose_name_plural = 'Parcelas'

    transacao_parcelada = models.ForeignKey(TransacaoParcelada, on_delete=models.CASCADE)
    numero_parcela = models.PositiveIntegerField(null=False, blank=True)
    valor_parcela = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    data = models.DateField(default=datetime.date.today)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(default=1, choices=[(1, 'Pendente'), (2, 'Paga'),])

    def __str__(self):
        return f'{self.transacao_parcelada.descricao} - R${self.valor_parcela} - {self.numero_parcela}ª Parcela'
    
    def get_usuario(self):
        return self.transacao_parcelada.usuario

class Transacao(models.Model):
    """
    Modelo para representar transações financeiras.
    """
    class Meta:
        db_table = 'transacao'
        verbose_name = 'Transacao'
        verbose_name_plural = 'Transacoes'
        
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE, verbose_name="conta", related_name="conta")
    data = models.DateField(default=datetime.date.today)
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=1, null=False, blank=False, default='D')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.SET_NULL, null=True, blank=True)
    conta_destino = models.ForeignKey(Conta, on_delete=models.CASCADE, null=True, blank=True, default=None, verbose_name="conta_destino", related_name="conta_destino")

    def __str__(self):
        return f'{self.descricao} - R${self.valor:.2f}'

    def resumo(self):
        """
        Retorna um resumo da transação em formato de string.
        """
        resumo = f'{self.data.strftime("%d/%m/%Y")}: {self.descricao}'
        if self.categoria:
            resumo += f' (Categoria: {self.categoria.nome})'
        if self.subcategoria:
            resumo += f' (Subcategoria: {self.subcategoria.nome})'
        resumo += f' - R${self.valor:.2f} ({self.get_tipo_display()})'
        return resumo

    def get_tipo_display(self):
        """
        Retorna a descrição do tipo de transação (Débito ou Crédito).
        """
        if self.tipo == 'D':
            return 'Despesa'
        else:
            return 'Receita'

