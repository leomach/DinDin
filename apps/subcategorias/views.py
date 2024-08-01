from django.shortcuts import render, redirect, get_object_or_404
from .models import Subcategoria, Categoria
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SubcategoriaForm

def listar_subcategorias(request, categoria_pk):
    """
    View para listar as subcategorias de uma categoria específica.
    """
    categoria = get_object_or_404(Categoria, pk=categoria_pk, usuario=request.user)
    subcategorias = Subcategoria.objects.filter(categoria=categoria)

    return render(request, 'categorias/subcategorias.html', {
        'categoria': categoria,
        'subcategorias': subcategorias
    })

@login_required
def criar_subcategoria(request, categoria_pk):
    """
    View para criar uma nova subcategoria para uma categoria específica.
    """
    categoria = get_object_or_404(Categoria, pk=categoria_pk, usuario=request.user)
    if request.method == 'POST':
        form = SubcategoriaForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            descricao = form.cleaned_data['descricao']

            try:
                subcategoria = Subcategoria.objects.create(
                    usuario=request.user,
                    categoria=categoria,
                    nome=nome,
                    descricao=descricao
                )
                subcategoria.save()

                messages.success(request, 'Subcategoria criada com sucesso!')
                return redirect('subcategorias', categoria_pk=categoria.pk)

            except Exception as e:
                messages.error(request, f'Erro ao criar subcategoria: {e}')
    else:
        form = SubcategoriaForm(user=request.user)

    return render(request, 'categorias/criar_subcategoria.html', {
        'categoria': categoria,
        'form': form
    })

@login_required
def editar_subcategoria(request, categoria_pk, subcategoria_pk):
    """
    View para editar uma subcategoria específica.
    """
    categoria = get_object_or_404(Categoria, pk=categoria_pk, usuario=request.user)
    subcategoria = get_object_or_404(Subcategoria, pk=subcategoria_pk, categoria=categoria)

    if request.method == 'POST':
        form = SubcategoriaForm(request.POST, instance=subcategoria)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            descricao = form.cleaned_data['descricao']

            try:
                subcategoria.nome = nome
                subcategoria.descricao = descricao
                subcategoria.save()

                messages.success(request, 'Subcategoria atualizada com sucesso!')
                return redirect('subcategorias', categoria_pk=categoria.pk)

            except Exception as e:
                messages.error(request, f'Erro ao editar subcategoria: {e}')
    else:
        form = SubcategoriaForm(instance=subcategoria, user=request.user)

    return render(request, 'categorias/editar_subcategoria.html', {
        'categoria': categoria,
        'subcategoria': subcategoria,
        'form': form
    })

@login_required
def excluir_subcategoria(request, categoria_pk, subcategoria_pk):
    """
    View para excluir uma subcategoria específica.
    """
    categoria = get_object_or_404(Categoria, pk=categoria_pk, usuario=request.user)
    subcategoria = get_object_or_404(Subcategoria, pk=subcategoria_pk, categoria=categoria)

    try:
        subcategoria.delete()
        messages.success(request, 'Subcategoria excluída com sucesso!')
        return redirect('subcategorias', categoria_pk=categoria.pk)

    except Exception as e:
        messages.error(request, f'Erro ao excluir subcategoria: {e}')

    return render(request, 'categorias/subcategorias.html', {
        'categoria': categoria,
        'subcategorias': Subcategoria.objects.filter(categoria=categoria)
    })
