from django.db import models
from ..categorias.models import Categoria

class Subcategoria(models.Model):
    """
    Modelo para representar subcategorias de transações.
    """
    nome = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='subcategorias')
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nome} ({self.categoria.nome})'
