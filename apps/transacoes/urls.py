from django.urls import path
from .views import listar_transacoes, criar_transacao, editar_transacao, \
    excluir_transacao, criar_transacao_parcelada, excluir_transacao_parcelada, listar_parcelas, \
    toggle_status_parcela, editar_parcela, get_subcategorias, duplicar_transacao, criar_transacao_transferencia, \
    editar_transacao_transferencia, excluir_transferencia, efetuar_transacao_modelo, listar_transacoes_modelo, criar_transacao_modelo, \
    editar_transacao_modelo, excluir_transacoes_modelo

urlpatterns = [
    path('transacoes/', listar_transacoes, name='listar_transacoes'),
    path('parcelas/', listar_parcelas, name='listar_parcelas'),
    path('criar_transacao/', criar_transacao, name='criar_transacao'),
    path('duplicar_transacao/<int:transacao_pk>/', duplicar_transacao, name='duplicar_transacao'),
    path('get_subcategorias/<int:categoria_id>/', get_subcategorias, name='get_subcategorias'),
    path('criar_transacao_parcelada/', criar_transacao_parcelada, name='criar_transacao_parcelada'),
    path('criar_transacao_transferencia/', criar_transacao_transferencia, name='criar_transacao_transferencia'),
    path('editar_transacao_transferencia/<int:transferencia_pk>/', editar_transacao_transferencia, name='editar_transacao_transferencia'),
    path('excluir_transferencia/<int:transferencia_pk>/', excluir_transferencia, name='excluir_transferencia'),
    path('editar_transacao/<int:transacao_pk>/', editar_transacao, name='editar_transacao'),
    path('editar_parcela/<int:parcela_pk>/', editar_parcela, name='editar_parcela'),
    path('toggle_status_parcela/<int:parcela_id>/', toggle_status_parcela, name='toggle_status_parcela'),
    path('excluir_transacao/<int:transacao_pk>/', excluir_transacao, name='excluir_transacao'),
    path('excluir_transacao_parcelada/<int:transacao_pk>/', excluir_transacao_parcelada, name='excluir_transacao_parcelada'),
    path('efetuar_transacao_modelo/<int:transacao_pk>/', efetuar_transacao_modelo, name='efetuar_transacao_modelo'),
    path('listar_transacoes_modelo/', listar_transacoes_modelo, name='listar_transacoes_modelo'),
    path('criar_transacao_modelo/', criar_transacao_modelo, name='criar_transacao_modelo'),
    path('editar_transacao_modelo/<int:transacao_pk>/', editar_transacao_modelo, name='editar_transacao_modelo'),
    path('excluir_transacao_modelo/<int:transacao_pk>/', excluir_transacoes_modelo, name='excluir_transacao_modelo'),
]
