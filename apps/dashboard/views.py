from django.shortcuts import render, redirect
from django.contrib import messages
from ..transacoes.models import Transacao
from..conta.models import Conta
from..categorias.models import Categoria
from..subcategorias.models import Subcategoria
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import datetime
from django.core.paginator import Paginator

def index(request):
    usuario = request.user
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    
    contas = Conta.objects.filter(usuario=usuario)
    transacoes = Transacao.objects.filter(usuario=usuario)
    categorias = Categoria.objects.filter(usuario=usuario)
    subcategorias = Subcategoria.objects.filter(usuario=usuario)
    
    # Data
    dia = datetime.now().date().day
    mes = datetime.now().date().month
    ano = datetime.now().date().year

    saldo_total_contas = Conta.objects.filter(usuario=usuario).aggregate(saldo_total=Sum('saldo_atual'))['saldo_total'] or 0
    saldo_total_transacoes = transacoes.aggregate(saldo_total=Sum('valor'))['saldo_total'] or 0
    diferenca_saldo = saldo_total_contas - saldo_total_transacoes

    # Calculos mês e ano atual
    transacoes_ano_atual = Transacao.objects.filter(data__year=ano)
    receitas_ano_atual = transacoes_ano_atual.filter(tipo='R').aggregate(saldo_total=Sum('valor'))['saldo_total'] or 0
    despesas_ano_atual = transacoes_ano_atual.filter(tipo='D').aggregate(saldo_total=Sum('valor'))['saldo_total'] or 0
    transacoes_mes_atual = Transacao.objects.filter(data__year=ano).filter(data__month=mes)
    receitas_mes_atual = transacoes_mes_atual.filter(tipo='R').aggregate(saldo_total=Sum('valor'))['saldo_total'] or 0
    despesas_mes_atual = transacoes_mes_atual.filter(tipo='D').aggregate(saldo_total=Sum('valor'))['saldo_total'] or 0
    saldo_mes_atual = receitas_mes_atual - despesas_mes_atual
    
    # Calculos mês e ano anterior
    transacoes_mes_anterior = Transacao.objects.filter(data__year=ano).filter(data__month=mes - 1)
    transacoes_ano_anterior = Transacao.objects.filter(data__year=ano - 1)
    receitas_mes_anterior = transacoes_mes_anterior.filter(tipo='R').aggregate(saldo_total=Sum('valor'))['saldo_total'] or 0
    despesas_mes_anterior = transacoes_mes_anterior.filter(tipo='D').aggregate(saldo_total=Sum('valor'))['saldo_total'] or 0
    receitas_ano_anterior = transacoes_ano_anterior.filter(tipo='R').aggregate(saldo_total=Sum('valor'))['saldo_total'] or 0
    despesas_ano_anterior = transacoes_ano_anterior.filter(tipo='D').aggregate(saldo_total=Sum('valor'))['saldo_total'] or 0
    saldo_mes_anterior = receitas_mes_anterior - despesas_mes_anterior
    saldo_ano_anterior = receitas_ano_anterior - despesas_ano_anterior

    # Gerais 2
    economia = saldo_mes_anterior + saldo_mes_atual

    # Faz a paginação das transações
    transacoes_paginator = Paginator(transacoes_mes_atual, 10)
    page_num = request.GET.get('page')
    page = transacoes_paginator.get_page(page_num)

    contexto = {
        'page': page,
        'contas': contas,
        'transacoes': transacoes,
        'categorias': categorias,
        'subcategorias': subcategorias,

        'data': {
            'dia': dia,
            'mes': mes,
            'ano': ano,
        },

        'economia':economia,
        'saldo_total_contas': saldo_total_contas,

        'diferenca_saldo': diferenca_saldo,
        'saldo_mes_atual': saldo_mes_atual,
        'receitas_mes_atual': receitas_mes_atual,
        'despesas_mes_atual': despesas_mes_atual,
        'receitas_ano_atual': receitas_ano_atual,
        'despesas_ano_atual': despesas_ano_atual,

        'receitas_mes_anterior': receitas_mes_anterior,
        'despesas_mes_anterior': despesas_mes_anterior,
        'saldo_mes_anterior': saldo_mes_anterior,
        'saldo_ano_anterior': saldo_ano_anterior,

        'transacoes_mes_atual': transacoes_mes_atual,
        'usuario': usuario,
    }
    return render(request, "dashboard/index.html", contexto)

