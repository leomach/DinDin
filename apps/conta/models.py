from django.db import models
from django.contrib.auth.models import User

class Conta(models.Model):
    """
    Modelo para representar contas bancárias e de investimento.
    """
    class Meta:
        db_table = 'conta'
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'

    nome = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255, blank=False, null=False)
    saldo_inicial = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    saldo_atual = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    limite = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    limite_atual = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    data_criacao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome