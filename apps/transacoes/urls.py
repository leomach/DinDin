from django.urls import path
from .views import listar_transacoes, criar_transacao, editar_transacao, excluir_transacao, criar_transacao_parcelada

urlpatterns = [
    path('transacoes/', listar_transacoes, name='listar_transacoes'),
    path('criar_transacao/', criar_transacao, name='criar_transacao'),
    path('criar_transacao_parcelada/', criar_transacao_parcelada, name='criar_transacao_parcelada'),
    path('editar_transacao/<int:transacao_pk>/', editar_transacao, name='editar_transacao'),
    path('excluir_transacao/<int:transacao_pk>/', excluir_transacao, name='excluir_transacao'),
]
