from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CategoriaForm
from django.core.paginator import Paginator

def listar_categorias(request):
    """
    View para listar todas as categorias do usuário logado.
    """
    usuario = request.user
    categorias = Categoria.objects.filter(usuario=usuario)

    categorias_paginator = Paginator(categorias, 10)
    page_num = request.GET.get('page')
    page = categorias_paginator.get_page(page_num)

    return render(request, 'categorias/categorias.html', {
        'categorias': page
    })

@login_required
def criar_categoria(request):
    """
    View para criar uma nova categoria.
    """
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            descricao = form.cleaned_data['descricao']
            tipo = form.cleaned_data['tipo']

            try:
                categoria = Categoria.objects.create(
                    usuario=request.user,
                    nome=nome,
                    descricao=descricao,
                    tipo=tipo,
                )
                categoria.save()

                messages.success(request, 'Categoria criada com sucesso!')
                return redirect('categorias')

            except Exception as e:
                messages.error(request, f'Erro ao criar categoria: {e}')
    else:
        form = CategoriaForm()

    return render(request, 'categorias/criar_categoria.html', {'form': form})

@login_required
def editar_categoria(request, categoria_id):
    """
    View para editar uma categoria específica.
    """
    categoria = get_object_or_404(Categoria, pk=categoria_id, usuario=request.user)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            descricao = form.cleaned_data['descricao']
            tipo = form.cleaned_data['tipo']
            
            categoria.nome = nome
            categoria.descricao = descricao
            categoria.tipo = tipo
            categoria.save()

            messages.success(request, 'Categoria atualizada com sucesso!')
            return redirect('categorias')
        else:
            messages.error(request, 'Formulário inválido.')
            return redirect('editar_categoria', categoria_id=categoria_id)
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'categorias/editar_categoria.html', {
        'form': form,
        'categoria': categoria
    })

@login_required
def excluir_categoria(request, categoria_id):
    """
    View para excluir uma categoria específica.
    """
    categoria = get_object_or_404(Categoria, pk=categoria_id, usuario=request.user)

    try:
        categoria.delete()
        messages.success(request, 'Categoria excluída com sucesso!')
        return redirect('categorias')

    except Exception as e:
        messages.error(request, f'Erro ao excluir categoria: {e}')

    return render(request, 'categorias/categorias.html')
