from django.urls import path
from apps.dashboard.views import \
    index, graficos_anuais

urlpatterns = [
    path('', index, name='index'),
    path('graficos/anuais/', graficos_anuais, name='graficos_anuais'),
]