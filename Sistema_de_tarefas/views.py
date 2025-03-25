from django.shortcuts import render
#@login_required
def login(request):
    # Lógica de login, se necessário
    return render(request, 'core/index.html')  # Renderiza o template de login
def registro(request):
    # Lógica de registro, se necessário
    return render(request, 'core/registro.html')  # Renderiza o template de registro

from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def minha_view(request):
    # Seu código aqui
    return render(request, 'template/index.html')  # Renderiza o template de login