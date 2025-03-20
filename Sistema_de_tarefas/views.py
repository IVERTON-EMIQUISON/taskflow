from django.shortcuts import render
#@login_required
def login(request):
    # Lógica de login, se necessário
    return render(request, 'core/index.html')  # Renderiza o template de login
def registro(request):
    # Lógica de registro, se necessário
    return render(request, 'core/registro.html')  # Renderiza o template de registro

from django.shortcuts import redirect

def lista_view(request):
    # Lógica para a página de lista, se necessário
    return render(request, os.path.join(os.path.dirname(__file__), '..', './template/lista.html'))

def deletar_view(request):
    # Lógica para a página de deletar, se necessário
    return render(request, os.path.join(os.path.dirname(__file__), '..', './template/deletar.html'))
def editar_view(request):
    # Lógica para a página de editar, se necesario
    return render(request, os.path.join(os.path.dirname(__file__), '..', './template/editar.html'))

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def minha_view(request):
    # Seu código aqui
    return render(request, 'template/index.html')  # Renderiza o template de login