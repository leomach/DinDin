from django.shortcuts import render, redirect, get_object_or_404
from .models import Transacao, TransacaoParcelada, Parcela
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from ..conta.models import Conta
from ..categorias.models import Categoria
from ..subcategorias.models import Subcategoria
from .forms import TransacaoForm, TransacaoParceladaForm
from django.core.paginator import Paginator
import datetime
from dateutil.relativedelta import *

def listar_transacoes(request):
    """
    View para listar as transações do usuário logado.
    """
    usuario = request.user
    
    # Busca as transações e transações parceladas separadamente
    transacoes = Transacao.objects.filter(usuario=usuario)
    transacoes_parceladas = TransacaoParcelada.objects.filter(usuario=usuario)

    def get_transacoes_e_parceladas(transacoes, transacoes_parceladas):
        # Combina as listas e ordena por data
        transacoes_e_parceladas = sorted(list(transacoes) + list(transacoes_parceladas), key=lambda obj: obj.data)
        return transacoes_e_parceladas
    
    transacoes_e_parceladas = get_transacoes_e_parceladas(transacoes=transacoes, transacoes_parceladas=transacoes_parceladas)

    # Calcula o saldo total das contas
    saldo_total_contas = Conta.objects.filter(usuario=usuario).aggregate(saldo_total=Sum('saldo_atual'))['saldo_total'] or 0

    # Calcula o saldo total das transações
    saldo_total_transacoes = transacoes.aggregate(saldo_total=Sum('valor'))['saldo_total'] or 0

    # Calcula a diferença entre os saldos
    diferenca_saldo = saldo_total_contas - saldo_total_transacoes

    # Faz a paginação das transações
    transacoes_paginator = Paginator(transacoes_e_parceladas, 10)
    page_num = request.GET.get('page')
    page = transacoes_paginator.get_page(page_num)

    return render(request, 'transacoes/listar_transacoes.html', {
        'page': page,
        'saldo_total_contas': saldo_total_contas,
        'saldo_total_transacoes': saldo_total_transacoes,
        'diferenca_saldo': diferenca_saldo,
    })


@login_required
def criar_transacao(request):
    """
    View para criar uma nova transação.
    """
    if request.method == 'POST':
        form = TransacaoForm(request.POST)

        if form.is_valid():
            usuario = request.user
            conta = get_object_or_404(Conta, pk=form.cleaned_data['conta'].id, usuario=usuario)
            data = form.cleaned_data['data']
            descricao = form.cleaned_data['descricao']
            valor = form.cleaned_data['valor']
            tipo = form.cleaned_data['tipo']
            categoria = form.cleaned_data['categoria']
            subcategoria = form.cleaned_data['subcategoria']

            try:
                if tipo == 'D':
                    conta.saldo_atual -= valor
                else:
                    conta.saldo_atual += valor

                conta.save()

                Transacao.objects.create(
                    usuario=usuario,
                    conta=conta,
                    data=data,
                    descricao=descricao,
                    valor=valor,
                    tipo=tipo,
                    categoria=categoria,
                    subcategoria=subcategoria
                )

                messages.success(request, 'Transação criada com sucesso!')
                return redirect('listar_transacoes')

            except Exception as e:
                messages.error(request, f'Erro ao criar transação: {e}')

    else:
        form = TransacaoForm()

    contas = Conta.objects.filter(usuario=request.user)
    categorias = Categoria.objects.filter(usuario=request.user)
    subcategorias = Subcategoria.objects.filter(usuario=request.user)

    return render(request, 'transacoes/criar_transacao.html', {
        'form': form,
        'contas': contas,
        'categorias': categorias,
        'subcategorias': subcategorias,
    })

@login_required
def criar_transacao_parcelada(request):
    """
    View para criar uma nova transação parcelada.
    """
    if request.method == 'POST':
        form = TransacaoParceladaForm(request.POST)

        if form.is_valid():
            usuario = request.user
            conta = get_object_or_404(Conta, pk=form.cleaned_data['conta'].id, usuario=usuario)
            data = form.cleaned_data['data']
            descricao = form.cleaned_data['descricao']
            valor = form.cleaned_data['valor_total']
            parcelas = form.cleaned_data['parcelas']
            categoria = form.cleaned_data['categoria']
            subcategoria = form.cleaned_data['subcategoria']

            #try:
            if conta.limite <= 0 or conta.limite_atual - valor >= conta.limite:
                messages.error(request, f'O limite da conta {conta.nome} não permite essa transação!')
                return redirect('listar_transacoes')
            conta.saldo_atual -= valor
            conta.limite_atual += valor
            conta.save()
            
            #try:
            trans_par = TransacaoParcelada.objects.create(
                usuario=usuario,
                conta=conta,
                data=data,
                descricao=descricao,
                valor_total=valor,
                parcelas=parcelas,
                categoria=categoria,
                subcategoria=subcategoria
            )

            if trans_par.id:
                #try:
                for i in range(1, int(parcelas) + 1):
                    Parcela.objects.create(
                        transacao_parcelada=get_object_or_404(TransacaoParcelada, pk=trans_par.id, usuario=usuario),
                        numero_parcela=i,
                        valor_parcela=valor / parcelas,
                        data=data + relativedelta(months=i)
                    )
                    messages.success(request, f'Parcela {i} criada com sucesso!')

                messages.success(request, 'Transação criada com sucesso!')
                return redirect('listar_transacoes')
                
                # except Exception as e:
                #     messages.error(request, f'Erro ao criar parcelas: {e}')
                #     return redirect('listar_transacoes')

        
            # except Exception as e:
            #     messages.error(request, f'Erro ao criar transação: {e}')

            # except Exception as e:
            #     messages.error(request, f'Erro ao criar transação: {e}')

    else:
        form = TransacaoParceladaForm()

    contas = Conta.objects.filter(usuario=request.user)
    categorias = Categoria.objects.filter(usuario=request.user)
    subcategorias = Subcategoria.objects.filter(usuario=request.user)

    return render(request, 'transacoes/criar_transacao_parcelada.html', {
        'form': form,
        'contas': contas,
        'categorias': categorias,
        'subcategorias': subcategorias,
    })

@login_required
def editar_transacao(request, transacao_pk):
    """
    View para editar uma transacao específica.
    """
    transacao = get_object_or_404(Transacao, pk=transacao_pk, usuario=request.user)

    if request.method == 'POST':
        form = TransacaoForm(request.POST, instance=transacao)

        if form.is_valid():
            conta = form.cleaned_data['conta']
            data = form.cleaned_data['data']
            descricao = form.cleaned_data['descricao']
            valor = form.cleaned_data['valor']
            tipo = form.cleaned_data['tipo']
            categoria = form.cleaned_data['categoria']
            subcategoria = form.cleaned_data['subcategoria']

            try:
                # Saldo antigo da transacao
                saldo_antigo = transacao.valor

                # Atualiza o saldo da conta de acordo com o novo valor e tipo da transacao
                if tipo == 'D':
                    conta.saldo_atual -= valor - saldo_antigo
                else:
                    conta.saldo_atual += valor - saldo_antigo

                conta.save()

                # Atualiza os dados da transacao
                transacao.conta = conta
                transacao.data = data
                transacao.descricao = descricao
                transacao.valor = valor
                transacao.tipo = tipo
                transacao.categoria = categoria
                transacao.subcategoria = subcategoria
                transacao.save()

                messages.success(request, 'Transação atualizada com sucesso!')
                return redirect('listar_transacoes')

            except Exception as e:
                messages.error(request, f'Erro ao editar transação: {e}')

    else:
        form = TransacaoForm(instance=transacao)

    contas = Conta.objects.filter(usuario=request.user)
    categorias = Categoria.objects.filter(usuario=request.user)
    subcategorias = Subcategoria.objects.filter(usuario=request.user)

    return render(request, 'transacoes/editar_transacao.html', {
        'form': form,
        'contas': contas,
        'categorias': categorias,
        'subcategorias': subcategorias,
        'transacao': transacao,
    })

@login_required
def excluir_transacao(request, transacao_pk):
    """
    View para excluir uma transacao específica.
    """
    transacao = get_object_or_404(Transacao, pk=transacao_pk, usuario=request.user)

    try:
        # Atualiza o saldo da conta após a exclusão da transacao
        if transacao.tipo == 'D':
            transacao.conta.saldo_atual += transacao.valor
        else:
            transacao.conta.saldo_atual -= transacao.valor

        transacao.conta.save()
        transacao.delete()

        messages.success(request, 'Transação excluída com sucesso!')
        return redirect('listar_transacoes')

    except Exception as e:
        messages.error(request, f'Erro ao excluir transação: {e}')
