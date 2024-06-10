from django.contrib import admin
from .models import Transacao, TransacaoParcelada, Parcela

admin.site.register(Transacao)
admin.site.register(TransacaoParcelada)
admin.site.register(Parcela)
