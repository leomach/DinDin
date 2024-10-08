from django.urls import path
from apps.conta.views import listar_contas, criar_conta, editar_conta, excluir_conta

urlpatterns = [
   path('contas', listar_contas, name='contas'),
   path('contas/criar/', criar_conta, name='criar_conta'),
   path('contas/editar/<int:conta_id>/', editar_conta, name='editar_conta'),
   path('contas/excluir/<int:conta_id>/', excluir_conta, name='excluir_conta'),
]