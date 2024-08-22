from django.shortcuts import render, redirect
from django.contrib import messages
from ..transacoes.models import Transacao, TransacaoParcelada, Parcela
from..conta.models import Conta
from..categorias.models import Categoria
from..subcategorias.models import Subcategoria
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import datetime
from django.core.paginator import Paginator

def get_lista1_lista2(lista1, lista2):
    # Combina as listas e ordena por data
    lista1_lista2 = sorted(list(lista1) + list(lista2), key=lambda obj: obj.data)
    return lista1_lista2

def index(request):
    usuario = request.user
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    
    contas = Conta.objects.filter(usuario=usuario)
    transacoes = Transacao.objects.filter(usuario=usuario)
    parcelas = Parcela.objects.filter(usuario=usuario)
    categorias = Categoria.objects.filter(usuario=usuario)
    categorias_despesas = categorias.filter(tipo=2)
    categorias_receitas = categorias.filter(tipo=1)
    subcategorias = Subcategoria.objects.filter(usuario=usuario)
    
    # Data
    dia = datetime.now().day
    mes = datetime.now().month
    ano = datetime.now().year

    # Transações do mês anterior
    if mes == 1:
        mes_anterior = 12
        ano_anterior = ano - 1
    else:
        mes_anterior = mes - 1
        ano_anterior = ano - 1


    saldo_total_contas = contas.aggregate(saldo_total=Sum('saldo_atual'))['saldo_total'] or 0


    if request.GET.get('time') == 'ano':
        transacoes_ano_atual = transacoes.filter(data__year=ano)
        parcelas_ano_atual = parcelas.filter(data__year=ano)
        transacoes_receitas_ano_atual = transacoes_ano_atual.filter(tipo='R').aggregate(saldo_total=Sum('valor'))['saldo_total'] or 0
        transacoes_despesas_ano_atual = transacoes_ano_atual.filter(tipo='D').aggregate(saldo_total=Sum('valor'))['saldo_total'] or 0
        total_parcelas_ano_atual = parcelas_ano_atual.aggregate(saldo_total=Sum('valor_parcela'))['saldo_total'] or 0
        despesas_ano_atual = transacoes_despesas_ano_atual + total_parcelas_ano_atual
    
        saldo_ano_atual = transacoes_receitas_ano_atual - despesas_ano_atual


        transacoes_ano_anterior = transacoes.filter(data__year=ano_anterior)
        parcelas_ano_anterior = parcelas.filter(data__year=ano_anterior)
        receitas_ano_anterior = transacoes_ano_anterior.filter(tipo='R').aggregate(saldo_total=Sum('valor'))['saldo_total'] or 0
        transacoes_despesas_ano_anterior = transacoes_ano_anterior.filter(tipo='D').aggregate(saldo_total=Sum('valor'))['saldo_total'] or 0
        parcelas_despesas_ano_anterior = parcelas_ano_anterior.aggregate(saldo_total=Sum('valor_parcela'))['saldo_total'] or 0
        despesas_ano_anterior = transacoes_despesas_ano_anterior + parcelas_despesas_ano_anterior

        saldo_ano_anterior = receitas_ano_anterior - despesas_ano_anterior

        economia_anual = saldo_ano_anterior + saldo_ano_atual

        c_receitas_anual = []
        c_despesas_anual = []
        for categoria in categorias_despesas:
            despesas_anual = transacoes_ano_atual.filter(categoria=categoria).aggregate(total=Sum('valor'))['total'] or 0
            despesas_parcelas_anual = parcelas_ano_atual.filter(transacao_parcelada__categoria=categoria).aggregate(saldo_total=Sum('valor_parcela'))['saldo_total'] or 0
            total_anual = despesas_anual + despesas_parcelas_anual
            c_despesas_anual.append({'nome': categoria.nome, 'total': total_anual})
        for categoria in categorias_receitas:
            receitas_anual = transacoes_ano_atual.filter(categoria=categoria).aggregate(total=Sum('valor'))['total'] or 0
            receitas_parcelas_anual = parcelas_ano_atual.filter(transacao_parcelada__categoria=categoria).aggregate(saldo_total=Sum('valor_parcela'))['saldo_total'] or 0
            total_anual = receitas_anual + receitas_parcelas_anual
            c_receitas_anual.append({'nome': categoria.nome, 'total': total_anual})

            contexto = {
                'usuario': usuario,
                'contas': contas,
                'transacoes': transacoes,
                'categorias': categorias,
                'subcategorias': subcategorias,

                'data': {
                    'dia': dia,
                    'mes': mes,
                    'ano': ano,
                },
                'saldo_total_contas': saldo_total_contas,

                'economia_anual':economia_anual,

                
                'c_despesas_anual': sorted(c_despesas_anual, key=lambda x: x['total'], reverse=True),
                'c_receitas_anual': sorted(c_receitas_anual, key=lambda x: x['total'], reverse=True),

                'saldo_ano_atual': saldo_ano_atual,
                'transacoes_receitas_ano_atual': transacoes_receitas_ano_atual,
                'despesas_ano_atual': despesas_ano_atual,

                'receitas_ano_anterior': receitas_ano_anterior,
                'despesas_ano_anterior': despesas_ano_anterior,
                'saldo_ano_anterior': saldo_ano_anterior,
            }
    else:
        transacoes_mes_atual = transacoes.filter(data__year=ano).filter(data__month=mes)
        parcelas_mes_atual = parcelas.filter(data__year=ano).filter(data__month=mes)
        transacoes_e_parcelas_mes_atual = get_lista1_lista2(lista1=transacoes_mes_atual, lista2=parcelas_mes_atual)

        transacoes_receitas_mes_atual = transacoes_mes_atual.filter(tipo='R').aggregate(saldo_total=Sum('valor'))['saldo_total'] or 0
        total_transacoes_despesas_mes_atual = transacoes_mes_atual.filter(tipo='D').aggregate(saldo_total=Sum('valor'))['saldo_total'] or 0
        total_parcelas_mes_atual = parcelas_mes_atual.aggregate(saldo_total=Sum('valor_parcela'))['saldo_total'] or 0
        despesas_mes_atual = total_transacoes_despesas_mes_atual + total_parcelas_mes_atual

        saldo_mes_atual = transacoes_receitas_mes_atual - despesas_mes_atual

    
        transacoes_mes_anterior = transacoes.filter(data__year=ano).filter(data__month=mes_anterior)
        parcelas_mes_anterior = parcelas.filter(data__year=ano).filter(data__month=mes_anterior)
        transacoes_e_parcelas_mes_anterior = get_lista1_lista2(lista1=transacoes_mes_anterior, lista2=parcelas_mes_anterior)

        transacoes_receitas_mes_anterior = transacoes_mes_anterior.filter(tipo='R').aggregate(saldo_total=Sum('valor'))['saldo_total'] or 0
        transacoes_despesas_mes_anterior = transacoes_mes_anterior.filter(tipo='D').aggregate(saldo_total=Sum('valor'))['saldo_total'] or 0
        total_parcelas_mes_anterior = parcelas_mes_anterior.aggregate(saldo_total=Sum('valor_parcela'))['saldo_total'] or 0
        despesas_mes_anterior = transacoes_despesas_mes_anterior + total_parcelas_mes_anterior

        saldo_mes_anterior = transacoes_receitas_mes_anterior - despesas_mes_anterior

        economia = saldo_mes_anterior + saldo_mes_atual

        transacoes_e_parcelas_mes_atual.sort(key=lambda x: x.data, reverse=True)

        # Faz a paginação das transações
        transacoes_paginator = Paginator(transacoes_e_parcelas_mes_atual, 10)
        page_num = request.GET.get('page')
        page_mes = transacoes_paginator.get_page(page_num)

        c_despesas = []
        c_receitas = []
        for categoria in categorias_despesas:
            despesas = transacoes_mes_atual.filter(categoria=categoria).aggregate(total=Sum('valor'))['total'] or 0
            despesas_parcelas = parcelas_mes_atual.filter(transacao_parcelada__categoria=categoria).aggregate(saldo_total=Sum('valor_parcela'))['saldo_total'] or 0
            total = despesas + despesas_parcelas
            c_despesas.append({'nome': categoria.nome, 'total': total})
        for categoria in categorias_receitas:
            receitas = transacoes_mes_atual.filter(categoria=categoria).aggregate(total=Sum('valor'))['total'] or 0
            receitas_parcelas = parcelas_mes_atual.filter(transacao_parcelada__categoria=categoria).aggregate(saldo_total=Sum('valor_parcela'))['saldo_total'] or 0
            total = receitas + receitas_parcelas
            c_receitas.append({'nome': categoria.nome, 'total': total})

            contexto = {
                'page': page_mes,
                'economia':economia,

                'c_despesas': sorted(c_despesas, key=lambda x: x['total'], reverse=True),
                'c_receitas': sorted(c_receitas, key=lambda x: x['total'], reverse=True),
                'saldo_mes_atual': saldo_mes_atual,
                'transacoes_receitas_mes_atual': transacoes_receitas_mes_atual,
                'despesas_mes_atual': despesas_mes_atual,
                'transacoes_receitas_mes_anterior': transacoes_receitas_mes_anterior,
                'transacoes_despesas_mes_anterior': transacoes_despesas_mes_anterior,
                'saldo_mes_anterior': saldo_mes_anterior,
                'despesas_mes_anterior': despesas_mes_anterior,
                'transacoes_mes_atual': transacoes_mes_atual,

                'usuario': usuario,
                'contas': contas,
                'transacoes': transacoes,
                'categorias': categorias,
                'subcategorias': subcategorias,

                'data': {
                    'dia': dia,
                    'mes': mes,
                    'ano': ano,
                },
                'saldo_total_contas': saldo_total_contas,
            }
    
    return render(request, "dashboard/index.html", contexto)

