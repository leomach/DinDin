from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CategoriaForm

def listar_categorias(request):
    """
    View para listar todas as categorias do usuário logado.
    """
    usuario = request.user
    categorias = Categoria.objects.filter(usuario=usuario)

    return render(request, 'categorias/categorias.html', {
        'categorias': categorias
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

            try:
                categoria = Categoria.objects.create(
                    usuario=request.user,
                    nome=nome,
                    descricao=descricao
                )
                categoria.save()

                messages.success(request, 'Categoria criada com sucesso!')
                return redirect('categorias')

            except Exception as e:
                messages.error(request, f'Erro ao criar categoria: {e}')
    else:
        form = CategoriaForm(user=request.user)

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

            try:
                categoria.nome = nome
                categoria.descricao = descricao
                categoria.save()

                messages.success(request, 'Categoria atualizada com sucesso!')
                return redirect('categorias')

            except Exception as e:
                messages.error(request, f'Erro ao editar categoria: {e}')

    else:
        form = CategoriaForm(instance=categoria, user=request.user)

    return render(request, 'categorias/editar_categoria.html', {
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
