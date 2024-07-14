from django.urls import path
from .views import listar_transacoes, criar_transacao, editar_transacao, \
    excluir_transacao, criar_transacao_parcelada, excluir_transacao_parcelada, listar_parcelas, \
    toggle_status_parcela, editar_parcela, get_subcategorias

urlpatterns = [
    path('transacoes/', listar_transacoes, name='listar_transacoes'),
    path('parcelas/', listar_parcelas, name='listar_parcelas'),
    path('criar_transacao/', criar_transacao, name='criar_transacao'),
    path('get_subcategorias/<int:categoria_id>/', get_subcategorias, name='get_subcategorias'),
    path('criar_transacao_parcelada/', criar_transacao_parcelada, name='criar_transacao_parcelada'),
    path('editar_transacao/<int:transacao_pk>/', editar_transacao, name='editar_transacao'),
    path('editar_parcela/<int:parcela_pk>/', editar_parcela, name='editar_parcela'),
    path('toggle_status_parcela/<int:parcela_id>/', toggle_status_parcela, name='toggle_status_parcela'),
    path('excluir_transacao/<int:transacao_pk>/', excluir_transacao, name='excluir_transacao'),
    path('excluir_transacao_parcelada/<int:transacao_pk>/', excluir_transacao_parcelada, name='excluir_transacao_parcelada'),
]
