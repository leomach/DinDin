from django.db import models

class Categoria(models.Model):
    """
    Modelo para representar categorias de transações.
    """
    nome = models.CharField(max_length=255, blank=False, null=False)
    descricao = models.CharField(max_length=255, blank=True)
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
