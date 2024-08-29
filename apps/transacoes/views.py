import datetime
from django.utils.timezone import make_aware, is_naive
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Transacao, TransacaoParcelada, Parcela, TransacaoModelo
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from ..conta.models import Conta
from ..categorias.models import Categoria
from ..subcategorias.models import Subcategoria
from .forms import TransacaoForm, TransacaoParceladaForm, ParcelaForm, TransferenciaForm, TransacaoModeloForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from dateutil.relativedelta import *

# Função auxiliar para converter qualquer data para datetime
def to_datetime(value):
    if isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
        value = datetime.datetime.combine(value, datetime.datetime.min.time())
    if is_naive(value):
        value = make_aware(value)
    return value

def listar_transacoes(request):
    """
    View para listar as transações do usuário logado.
    """
    usuario = request.user
    
    # Busca as transações e transações parceladas separadamente
    transacoes = Transacao.objects.filter(usuario=usuario)
    transacoes_parceladas = TransacaoParcelada.objects.filter(usuario=usuario)
    transacoes_modelo = TransacaoModelo.objects.filter(usuario=usuario)

    # Verifica se tem GET para search e filtra as transações
    if request.GET.get('search'):
        search = request.GET.get('search')
        transacoes = transacoes.filter(descricao__icontains=search)
        transacoes_parceladas = transacoes_parceladas.filter(descricao__icontains=search)

    def get_transacoes_e_parceladas(transacoes, transacoes_parceladas):
        transacoes_e_parceladas = sorted(
            list(transacoes) + list(transacoes_parceladas),
            key=lambda obj: datetime.datetime.combine(obj.data, datetime.datetime.min.time()) if isinstance(obj.data, datetime.date) else obj.data
        )
        return transacoes_e_parceladas
    
    transacoes_e_parceladas = get_transacoes_e_parceladas(transacoes=transacoes, transacoes_parceladas=transacoes_parceladas)
    transacoes_e_parceladas = sorted(
        list(transacoes) + list(transacoes_parceladas),
        key=lambda obj: to_datetime(obj.data),
        reverse=True
    )

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
        'transacoes_modelo': transacoes_modelo,
        'saldo_total_contas': saldo_total_contas,
        'saldo_total_transacoes': saldo_total_transacoes,
        'diferenca_saldo': diferenca_saldo,
    })

@login_required
def listar_parcelas(request):
    usuario = request.user


    pago_ou_pendente = request.GET.get('pago')
    print(pago_ou_pendente)
    if pago_ou_pendente == 'true':
        parcelas = Parcela.objects.filter(usuario=usuario).filter(status=2)
    elif pago_ou_pendente == 'false':
        parcelas = Parcela.objects.filter(usuario=usuario).filter(status=1)
    else:
        parcelas = Parcela.objects.filter(usuario=usuario)
        
    parcelas_decrescente = sorted(parcelas, key=lambda x: x.data, reverse=False)

    parcelas_paginator = Paginator(parcelas_decrescente, 10)
    page_num = request.GET.get('page')
    page = parcelas_paginator.get_page(page_num)

    return render(request, 'transacoes/listar_parcelas.html', {
        'page': page,
    })

@login_required
def toggle_status_parcela(request, parcela_id):
    parcela = get_object_or_404(Parcela, pk=parcela_id, usuario=request.user)
    conta = get_object_or_404(Conta, pk=parcela.transacao_parcelada.conta.id, usuario=request.user)

    if parcela.status == 1:
        valor_do_limite = conta.limite_atual + parcela.valor_parcela
        conta.limite_atual = valor_do_limite
    else:
        valor_do_limite = conta.limite_atual - parcela.valor_parcela
        conta.limite_atual = valor_do_limite

    parcela.status = not parcela.status
    parcela.save()
    conta.save()

    messages.success(request, 'Status da parcela alterado com sucesso.')
    return redirect('listar_parcelas')


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

            if tipo == 'D':
                valor_da_conta = conta.saldo_atual - valor
                conta.saldo_atual = valor_da_conta
            else:
                valor_da_conta = conta.saldo_atual + valor
                conta.saldo_atual = valor_da_conta

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

    else:
        form = TransacaoForm(user=request.user)

    contas = Conta.objects.filter(usuario=request.user)
    categorias = Categoria.objects.filter(usuario=request.user)
    subcategorias = Subcategoria.objects.filter(usuario=request.user)

    return render(request, 'transacoes/criar_transacao.html', {
        'form': form,
        'contas': contas,
        'categorias': categorias,
        'subcategorias': subcategorias,
    })

def get_subcategorias(request, categoria_id):
    subcategorias = list(Subcategoria.objects.filter(categoria_id=categoria_id).values('id', 'nome'))
    return JsonResponse(subcategorias, safe=False)

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
            if conta.limite <= 0 or conta.limite_atual - valor < 0:
                messages.error(request, f'O limite da conta {conta.nome} não permite essa transação!')
                return redirect('listar_transacoes')
            valor_da_conta = conta.saldo_atual - valor
            conta.saldo_atual = valor_da_conta
            valor_do_limite = conta.limite_atual - valor
            conta.limite_atual = valor_do_limite
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
                        data=data + relativedelta(months=i),
                        usuario=usuario
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
        form = TransacaoParceladaForm(user=request.user)

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
def criar_transacao_transferencia(request):
    """
    View para criar uma nova transferência.
    """
    if request.method == 'POST':
        form = TransferenciaForm(request.POST)

        if form.is_valid():
            usuario = request.user
            conta = form.cleaned_data['conta']
            conta_destino = form.cleaned_data['conta_destino']
            data = form.cleaned_data['data']
            descricao = form.cleaned_data['descricao']
            valor = form.cleaned_data['valor']
            tipo = 'T'
            categoria = form.cleaned_data['categoria']
            subcategoria = form.cleaned_data['subcategoria']

            valor_da_conta = conta.saldo_atual - valor
            conta.saldo_atual = valor_da_conta
            valor_da_conta_destino = conta_destino.saldo_atual + valor
            conta_destino.saldo_atual = valor_da_conta_destino

            conta.save()
            conta_destino.save()

            Transacao.objects.create(
                usuario=usuario,
                conta=conta,
                conta_destino=conta_destino,
                data=data,
                descricao=descricao,
                valor=valor,
                tipo=tipo,
                categoria=categoria,
                subcategoria=subcategoria
            )

            messages.success(request, 'Transação criada com sucesso!')
            return redirect('listar_transacoes')

    else:
        form = TransferenciaForm(user=request.user)

    return render(request, 'transacoes/criar_transferencia.html', {
        'form': form,
    })

@login_required
def editar_transacao_transferencia(request, transacao_pk):
    """
    View para editar uma transacao de transferencia específica.
    """
    transacao = get_object_or_404(Transacao, pk=transacao_pk, usuario=request.user, tipo='T')
    usuario = request.user

    if request.method == 'POST':
        form = TransferenciaForm(request.POST, instance=transacao)

        if form.is_valid():
            conta = form.cleaned_data['conta']
            conta_destino = form.cleaned_data['conta_destino']
            data = form.cleaned_data['data']
            descricao = form.cleaned_data['descricao']
            valor = form.cleaned_data['valor']
            tipo = 'T'
            categoria = form.cleaned_data['categoria']
            subcategoria = form.cleaned_data['subcategoria']

            # Atualiza o saldo das contas
            valor_da_transacao_antiga = transacao.valor
            valor_da_conta_origem_antiga = transacao.conta.saldo_atual + valor_da_transacao_antiga
            valor_da_conta_destino_antiga = transacao.conta_destino.saldo_atual - valor_da_transacao_antiga
            transacao.conta.saldo_atual = valor_da_conta_origem_antiga
            transacao.conta_destino.saldo_atual = valor_da_conta_destino_antiga
            transacao.conta.save()
            transacao.conta_destino.save()

            valor_da_conta = conta.saldo_atual - valor
            conta.saldo_atual = valor_da_conta
            valor_da_conta_destino = conta_destino.saldo_atual + valor
            conta_destino.saldo_atual = valor_da_conta_destino

            conta.save()
            conta_destino.save()

            # Atualiza a transacao
            transacao.conta = conta
            transacao.conta_destino = conta_destino
            transacao.data = data
            transacao.descricao = descricao
            transacao.valor = valor
            transacao.tipo = tipo
            transacao.categoria = categoria
            transacao.subcategoria = subcategoria
            transacao.save()
            
            messages.success(request, 'Transação editada com sucesso!')
            return redirect('listar_transacoes')
        else:
            form = TransferenciaForm(instance=transacao)
    else:
        form = TransferenciaForm(instance=transacao)
        return render(request, 'transacoes/editar_transferencia.html', {'form': form})

@login_required
def editar_transacao(request, transacao_pk):
    """
    View para editar uma transacao específica.
    """
    transacao = get_object_or_404(Transacao, pk=transacao_pk, usuario=request.user)
    usuario = request.user

    if request.method == 'POST':
        form = TransacaoForm(request.POST, instance=transacao)

        if form.is_valid():
            conta = get_object_or_404(Conta, pk=form.cleaned_data['conta'].id, usuario=usuario)
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
                    valor_da_conta = conta.saldo_atual + saldo_antigo - valor
                    conta.saldo_atual = valor_da_conta
                else:
                    valor_da_conta = conta.saldo_atual - saldo_antigo + valor
                    conta.saldo_atual = valor_da_conta

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
        form = TransacaoForm(instance=transacao, user=request.user)

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
def duplicar_transacao(request, transacao_pk):
    """
    View para duplicar uma transacao específica.
    """
    transacao = get_object_or_404(Transacao, pk=transacao_pk, usuario=request.user)
    usuario = request.user

    if request.method == 'POST':
        form = TransacaoForm(request.POST, instance=transacao)

        if form.is_valid():
            conta = get_object_or_404(Conta, pk=form.cleaned_data['conta'].id, usuario=usuario)
            data = form.cleaned_data['data']
            descricao = form.cleaned_data['descricao']
            valor = form.cleaned_data['valor']
            tipo = form.cleaned_data['tipo']
            categoria = form.cleaned_data['categoria']
            subcategoria = form.cleaned_data['subcategoria']

            try:
                if tipo == 'D':
                    valor_da_conta = conta.saldo_atual - valor
                    conta.saldo_atual = valor_da_conta
                else:
                    valor_da_conta = conta.saldo_atual + valor
                    conta.saldo_atual = valor_da_conta

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

                messages.success(request, 'Transação duplicada com sucesso!')
                return redirect('listar_transacoes')

            except Exception as e:
                messages.error(request, f'Erro ao editar transação: {e}')

    else:
        form = TransacaoForm(instance=transacao, user=request.user)

    contas = Conta.objects.filter(usuario=request.user)
    categorias = Categoria.objects.filter(usuario=request.user)
    subcategorias = Subcategoria.objects.filter(usuario=request.user)

    return render(request, 'transacoes/duplicar_transacao.html', {
        'form': form,
        'contas': contas,
        'categorias': categorias,
        'subcategorias': subcategorias,
        'transacao': transacao,
    })

def editar_parcela(request, parcela_pk):
    """
    View para editar uma parcela específica.
    """
    usuario = request.user
    parcela = get_object_or_404(Parcela, pk=parcela_pk, usuario=usuario)
    conta = get_object_or_404(Conta, pk=parcela.transacao_parcelada.conta.id, usuario=usuario)

    if request.method == 'POST':
        form = ParcelaForm(request.POST, instance=parcela)

        if form.is_valid():
            data = form.cleaned_data['data']
            valor_parcela = form.cleaned_data['valor_parcela']

            parcela.data = data
            saldo_atual_conta = conta.saldo_atual - parcela.valor_parcela + valor_parcela
            limite_atual_conta = conta.limite_atual + parcela.valor_parcela - valor_parcela
            conta.saldo_atual = saldo_atual_conta
            conta.limite_atual = limite_atual_conta

            conta.save()
            parcela.save()
            messages.success(request, 'Parcela atualizada com sucesso!')
            return redirect('listar_parcelas')
        else:
            messages.error(request, f'Erro: Formulário inválido')
            return redirect('editar_parcela', parcela_pk=parcela_pk)
    else:
        form = ParcelaForm(instance=parcela)
    
    return render(request, 'transacoes/editar_parcela.html', {
        'form': form,
        'parcela': parcela,
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
            valor_da_conta = transacao.conta.saldo_atual + transacao.valor
            transacao.conta.saldo_atual = valor_da_conta
        else:
            valor_da_conta = transacao.conta.saldo_atual - transacao.valor
            transacao.conta.saldo_atual = valor_da_conta

        transacao.conta.save()
        transacao.delete()

        messages.success(request, 'Transação excluída com sucesso!')
        return redirect('listar_transacoes')

    except Exception as e:
        messages.error(request, f'Erro ao excluir transação: {e}')

@login_required
def excluir_transacao_parcelada(request, transacao_pk):
    """
    View para excluir uma transacao específica.
    """
    transacao = get_object_or_404(TransacaoParcelada, pk=transacao_pk, usuario=request.user)

    try:
        # Atualiza o saldo da conta após a exclusão da transacao
        valor_da_conta = transacao.conta.saldo_atual + transacao.valor_total
        transacao.conta.saldo_atual = valor_da_conta

        valor_do_limite = transacao.conta.limite_atual + transacao.valor_total
        transacao.conta.limite_atual = valor_do_limite

        transacao.conta.save()
        transacao.delete()

        messages.success(request, 'Transação parcelada excluída com sucesso!')
        return redirect('listar_transacoes')

    except Exception as e:
        messages.error(request, f'Erro ao excluir transação: {e}')
        return HttpResponse(f"Erro: {e}")
    
@login_required
def excluir_transferencia(request, transacao_pk):
    """
    View para excluir uma transferencia específica.
    """
    transacao = get_object_or_404(Transacao, pk=transacao_pk, usuario=request.user, tipo='T')

    # Atualiza o saldo das contas de origem e destino após a exclusão da transferencia
    saldo_da_conta_origem = transacao.conta.saldo_atual + transacao.valor
    transacao.conta.saldo_atual = saldo_da_conta_origem
    saldo_da_conta_destino = transacao.conta_destino.saldo_atual - transacao.valor
    transacao.conta_destino.saldo_atual = saldo_da_conta_destino
    transacao.conta.save()
    transacao.conta_destino.save()
    transacao.delete()

    messages.success(request, 'Transferência excluída com sucesso!')
    return redirect('listar_transacoes')

@login_required
def listar_transacoes_modelo(request):
    """
    View para listar transacoes modelo.
    """
    usuario = request.user
    transacoes = TransacaoModelo.objects.filter(usuario=usuario)

    return render(request, 'transacoes/listar_transacoes_modelo.html', {'transacoes': transacoes})

@login_required
def criar_transacao_modelo(request):
    """
    View para criar um novo modelo de transacao.
    """
    usuario = request.user
    if request.method == 'POST':
        form = TransacaoModeloForm(request.POST, user=usuario)

        if form.is_valid():
            conta = get_object_or_404(Conta, pk=form.cleaned_data['conta'].id, usuario=usuario)
            descricao = form.cleaned_data['descricao']
            valor = form.cleaned_data['valor']
            tipo = form.cleaned_data['tipo']
            categoria = form.cleaned_data['categoria']
            subcategoria = form.cleaned_data['subcategoria']

            TransacaoModelo.objects.create(
                usuario=usuario,
                conta=conta,
                descricao=descricao,
                valor=valor,
                tipo=tipo,
                categoria=categoria,
                subcategoria=subcategoria,
            )

            messages.success(request, 'Modelo de transacao criado com sucesso!')
            return redirect('listar_transacoes_modelo')
        else:
            messages.error(request, 'Erro: Formulário inválido')
            return redirect('criar_transacao_modelo')
    else:
        form = TransacaoModeloForm(user=usuario)

    return render(request, 'transacoes/criar_transacao_modelo.html', {'form': form})

@login_required
def editar_transacao_modelo(request, transacao_pk):
    """
    View para editar um modelo de transacao.
    """
    transacao_modelo = get_object_or_404(TransacaoModelo, pk=transacao_pk, usuario=request.user)

    if request.method == 'POST':
        form = TransacaoModeloForm(request.POST, instance=transacao_modelo, user=request.user)

        if form.is_valid():
            usuario = request.user
            conta = get_object_or_404(Conta, pk=form.cleaned_data['conta'].id, usuario=usuario)
            descricao = form.cleaned_data['descricao']
            valor = form.cleaned_data['valor']
            tipo = form.cleaned_data['tipo']
            categoria = form.cleaned_data['categoria']
            subcategoria = form.cleaned_data['subcategoria']

            transacao_modelo.conta = conta
            transacao_modelo.descricao = descricao
            transacao_modelo.valor = valor
            transacao_modelo.tipo = tipo
            transacao_modelo.categoria = categoria
            transacao_modelo.subcategoria = subcategoria
            transacao_modelo.save()

            messages.success(request, 'Modelo de transacao editado com sucesso!')
            return redirect('criar_transacao_modelo')
        else:
            messages.error(request, 'Erro: Formulário inválido')
            return redirect('editar_transacao_modelo', transacao_pk=transacao_pk)
    else:
        form = TransacaoModeloForm(instance=transacao_modelo, user=request.user)

    return render(request, 'transacoes/editar_transacao_modelo.html', {'form': form})

@login_required
def efetuar_transacao_modelo(request, transacao_pk):
    """
    View para efetuar uma transacao a partir de um modelo de transacao.
    """

    if request.method == 'POST':
        usuario = request.user
        transacao_modelo = get_object_or_404(TransacaoModelo, pk=transacao_pk, usuario=usuario)
        conta = transacao_modelo.conta
        data = datetime.datetime.now()
        descricao = transacao_modelo.descricao
        valor = transacao_modelo.valor
        tipo = transacao_modelo.tipo
        categoria = transacao_modelo.categoria
        subcategoria = transacao_modelo.subcategoria
        quantidade = request.POST['quantidade']

        for t in range(int(quantidade)):
            Transacao.objects.create(
                usuario=usuario,
                conta=conta,
                data=data,
                descricao=descricao,
                valor=valor,
                tipo=tipo,
                categoria=categoria,
                subcategoria=subcategoria,
            )
        
        messages.success(request, 'Transações criadas com sucesso!')
        return redirect('listar_transacoes')
    else:
        messages.error(request, 'Você deve preencher o formulário de modelo de transação.')
        return redirect('listar_transacoes')
    
@login_required
def excluir_transacoes_modelo(request, transacao_pk):
    """
    View para excluir transacoes modelo.
    """
    transacao_modelo = get_object_or_404(TransacaoModelo, pk=transacao_pk, usuario=request.user)
    transacao_modelo.delete()
    messages.success(request, 'Modelo de transacoes excluído com sucesso!')
    return redirect('listar_transacoes_modelo')
    