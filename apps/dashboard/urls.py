from django.urls import path
from apps.dashboard.views import \
    index, relatorio_mes, relatorios, relatorio_dia, relatorio_vencedor, relatorio_liquido

urlpatterns = [
    path('', index, name='index'),
    path('relatorios/', relatorios, name='relatorios'),
    path('relatorio-dia/', relatorio_dia, name='relatorio_dia'),
    path('relatorio/mes/', relatorio_mes, name='relatorio_mes'),
    path('relatorio-vencedor/', relatorio_vencedor, name='relatorio_vencedor'),
    path('relatorio-liquido/', relatorio_liquido, name='relatorio_liquido'),
]