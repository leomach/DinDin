from django.urls import path
from apps.subcategorias.views import listar_subcategorias, criar_subcategoria, editar_subcategoria, excluir_subcategoria

urlpatterns = [
    path('subcategorias/<int:categoria_pk>', listar_subcategorias, name='subcategorias'),
    path('criar_subcategoria/<int:categoria_pk>', criar_subcategoria, name='criar_subcategoria'),
    path('subcategorias/editar/<int:categoria_pk>/<int:subcategoria_pk>', editar_subcategoria, name='editar_subcategoria'),
    path('subcategorias/excluir/<int:categoria_pk>/<int:subcategoria_pk>', excluir_subcategoria, name='excluir_subcategoria'),
]