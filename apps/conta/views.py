from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from .models import Conta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.conta.forms import ContaForms

def listar_contas(request):
    """
    View para listar todas as contas do usuário logado.
    """
    usuario = request.user
    contas = Conta.objects.filter(usuario=usuario)
    return render(request, 'contas/contas.html', {'contas': contas, 'usuario': usuario})

@login_required
def criar_conta(request):
    """
    View para criar uma nova conta para o usuário logado.
    """
    if request.method == 'POST':
        form = ContaForms(request.POST)

        if form.is_valid():
            nome = form.cleaned_data['nome']
            descricao = form.cleaned_data['descricao']
            saldo_inicial = form.cleaned_data['saldo_inicial']
            limite = form.cleaned_data['limite']

            try:
                saldo_inicial = float(saldo_inicial)
            except ValueError:
                messages.error(request, 'Saldo inicial inválido.')
                return redirect('contas')

            usuario = request.user

            Conta.objects.create(
                usuario=usuario,
                nome=nome,
                descricao=descricao,
                saldo_atual=saldo_inicial,
                limite=limite,
                limite_atual=limite
            )

            messages.success(request, 'Conta criada com sucesso!')
            return redirect('contas')
    else:
        form = ContaForms()

    return render(request, 'contas/criar_conta.html', {'form': form})

@login_required
def editar_conta(request, conta_id):
    """
    View para editar uma conta específica do usuário logado.
    """
    conta = get_object_or_404(Conta, pk=conta_id, usuario=request.user)

    if request.method == 'POST':
        form = ContaForms(request.POST, instance=conta)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            descricao = form.cleaned_data['descricao']
            saldo_inicial = form.cleaned_data['saldo_inicial']
            limite = form.cleaned_data['limite']

            try:
                saldo_inicial = float(saldo_inicial)
            except ValueError:
                messages.error(request, 'Saldo atual inválido.')
                return redirect('editar_conta', pk=conta.pk)

            conta.nome = nome
            conta.descricao = descricao
            conta.saldo_inicial = saldo_inicial
            conta.limite = limite
            conta.save()
            messages.success(request, 'Conta atualizada com sucesso!')
            return redirect('contas')
    else:
        form = ContaForms(instance=conta)

    return render(request, 'contas/editar_conta.html', {'form': form, 'conta': conta})

@login_required
def excluir_conta(request, conta_id):
    """
    View para excluir uma conta específica do usuário logado.
    """
    conta = get_object_or_404(Conta, pk=conta_id, usuario=request.user)
    conta.delete()
    messages.success(request, 'Conta excluída com sucesso!')
    return redirect('contas')
