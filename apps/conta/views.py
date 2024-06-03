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
def template_criar(request):
    """
    View para renderizar o template de criação de conta.
    """
    form = ContaForms
    return render(request, 'contas/criar_conta.html', {'form': form})

@login_required
def criar_conta(request):
    """
    View para criar uma nova conta para o usuário logado.
    """
    if request.method == 'POST':
        nome = request.POST['nome']
        descricao = request.POST['descricao']
        saldo_inicial = request.POST['saldo_inicial']

        try:
            saldo_inicial = float(saldo_inicial)
        except ValueError:
            messages.error(request, 'Saldo inicial inválido.')
            return redirect('contas')

        usuario = request.user
        conta = Conta.objects.create(usuario=usuario, nome=nome, descricao=descricao, saldo_atual=saldo_inicial)
        conta.save()
        messages.success(request, 'Conta criada com sucesso!')
        return redirect('contas')

    return render(request, 'contas/criar_conta.html')

@login_required
def editar_conta(request, conta_id):
    """
    View para editar uma conta específica do usuário logado.
    """
    conta = get_object_or_404(Conta, pk=conta_id, usuario=request.user)

    if request.method == 'POST':
        nome = request.POST['nome']
        descricao = request.POST['descricao']
        saldo_atual = request.POST['saldo_atual']

        try:
            saldo_atual = float(saldo_atual)
        except ValueError:
            messages.error(request, 'Saldo atual inválido.')
            return redirect('editar_conta', pk=conta.pk)

        conta.nome = nome
        conta.descricao = descricao
        conta.saldo_atual = saldo_atual
        conta.save()
        messages.success(request, 'Conta atualizada com sucesso!')
        return redirect('contas')

    return render(request, 'contas/editar_conta.html', {'conta': conta})

@login_required
def excluir_conta(request, conta_id):
    """
    View para excluir uma conta específica do usuário logado.
    """
    conta = get_object_or_404(Conta, pk=conta_id, usuario=request.user)
    conta.delete()
    messages.success(request, 'Conta excluída com sucesso!')
    return redirect('contas')
