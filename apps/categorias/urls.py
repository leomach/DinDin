from django.urls import path
from apps.categorias.views import listar_categorias, criar_categoria, editar_categoria, excluir_categoria

urlpatterns = [
    path('categorias', listar_categorias, name='categorias'),
    path('criar_categoria', criar_categoria, name='criar_categoria'),
    path('categorias/editar/<int:categoria_id>', editar_categoria, name='editar_categoria'),
    path('categorias/excluir/<int:categoria_id>', excluir_categoria, name='excluir_categoria'),
]