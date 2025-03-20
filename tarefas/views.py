
from django.shortcuts import render, redirect, get_object_or_404  
from django.contrib.auth.decorators import login_required  
from .models import Tarefa, Categoria  
from .forms import TarefaForm  
from .models import Status  # Add this line to import Status
from django.utils import timezone 
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

@login_required  
def lista_tarefas(request):  
    # Obtém todas as tarefas do usuário filtradas por status  
    tarefas = Tarefa.objects.filter(usuario=request.user)  

    tarefas_pendentes = tarefas.filter(status=Status.PENDENTE, concluida=False).order_by('prazo')  
    tarefas_planejadas = tarefas.filter(status=Status.PLANEJADA, concluida=False).order_by('prazo')  
    tarefas_em_andamento = tarefas.filter(status=Status.EM_ANDAMENTO, concluida=False).order_by('prazo')  
    tarefas_aguardando_aprovacao = tarefas.filter(status=Status.AGUARDANDO_APROVACAO, concluida=False).order_by('prazo')  
    tarefas_concluidas = tarefas.filter(concluida=True).order_by('-criada_em')  

    # Contexto com todas as tarefas filtradas por status  
    context = {  
        'tarefas_pendentes': tarefas_pendentes,  
        'tarefas_planejadas': tarefas_planejadas,  
        'tarefas_em_andamento': tarefas_em_andamento,  
        'tarefas_aguardando_aprovacao': tarefas_aguardando_aprovacao,  
        'tarefas_concluidas': tarefas_concluidas,  
    }  

    # Renderiza a página com o contexto  
    return render(request, 'tarefas/lista.html', context)  
@login_required
def criar_tarefa(request):
    
    if request.method == "POST":
        form = TarefaForm(request.POST)
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.usuario = request.user
            
            # Capturar categoria do formulário
            categoria_id = request.POST.get("categoria")
            if categoria_id:
                tarefa.categoria = get_object_or_404(Categoria, id=categoria_id)
           
            # Garantindo que o prazo seja interpretado corretamente
            prazo = request.POST.get("prazo")
            if prazo:
                tarefa.prazo = prazo  # Django já entende o formato recebido
                
            tarefa.save()
            return JsonResponse({"message": "Tarefa criada com sucesso!"}, status=201)

        return JsonResponse({"error": "Dados inválidos"}, status=400)

    categorias = Categoria.objects.all()
    status_opcoes = [status[0] for status in Status.choices]  # Pegando os valores dos status

    return render(request, "tarefas/criar.html", {
        "categorias": categorias,
        "status_opcoes": status_opcoes  # Enviando status para o template
    })
    
@login_required
def buscar_tarefa_por_titulo(request):  
    titulo = request.GET.get('titulo', '')  
    tarefa = Tarefa.objects.filter(titulo=titulo).first()  

    if tarefa:  
        response_data = {  
            'id': tarefa.id,  
            'titulo': tarefa.titulo,  
            'descricao': tarefa.descricao,  
            'prazo': tarefa.prazo,  
            'categoria': tarefa.categoria_id,  # Ou outro campo que represente a categoria  
            'status': tarefa.status,  
        }  
        return JsonResponse(response_data)  
    else:  
        return JsonResponse({'error': 'Tarefa não encontrada'}, status=404)  
    
from .models import Tarefa

def get_valid_task_id(usuario):
    """Retorna um ID válido de uma tarefa do usuário ou None se não houver tarefas"""
    tarefa_valida = Tarefa.objects.filter(usuario=usuario).first()
    return tarefa_valida.id if tarefa_valida else None

@login_required
def editar_tarefa(request, id):
    """Edita uma tarefa existente"""
    
    if not Tarefa.objects.filter(id=id, usuario=request.user).exists():
        id = get_valid_task_id(request.user)  # Obtém um novo ID válido
    
    if not id:  # Se ainda não houver um ID válido, redireciona para a lista de tarefas
        return HttpResponseRedirect("/tarefas/") 
    
    tarefa = get_object_or_404(Tarefa, id=id, usuario=request.user)

    if request.method == "POST":
        form = TarefaForm(request.POST, instance=tarefa)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Tarefa atualizada com sucesso!"}, status=200)
        return JsonResponse({"error": "Dados inválidos"}, status=400)

    categorias = Categoria.objects.all()
    status_opcoes = [status[0] for status in Status.choices]
        
    return render(request, "tarefas/editar.html", {
        "tarefa": tarefa,
        "categorias": categorias,
        "status_opcoes": status_opcoes
    })
    
@login_required  
def concluir_tarefa(request, tarefa_id):  
    """ Endpoint para concluir uma tarefa e arquivá-la """  
    tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)  

    if tarefa.concluida:  
        return JsonResponse({"message": "Tarefa já está concluída."}, status=400)  

    tarefa.concluir_tarefa()  # Chama o método que marca a tarefa como concluída e a arquiva  
    return JsonResponse({"message": "Tarefa concluída e arquivada com sucesso!"})  

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Tarefa, Status

@api_view(['PATCH'])  
@login_required  
def atualizar_status(request, pk):  
    try:  
        tarefa = Tarefa.objects.get(pk=pk, usuario=request.user)  
    except Tarefa.DoesNotExist:  
        return Response({"erro": "Tarefa não encontrada"}, status=status.HTTP_404_NOT_FOUND)  

    novo_status = request.data.get('status')  
    if novo_status not in dict(Status.choices):  # Verificação com Status, não com Tarefa  
        return Response({"erro": "Status inválido"}, status=status.HTTP_400_BAD_REQUEST)  

    tarefa.status = novo_status  
    tarefa.save()  
    return Response({"message": "Status atualizado com sucesso!"}, status=status.HTTP_200_OK)  
    
from django.shortcuts import render, redirect  

@login_required  
def deletar_tarefa(request, tarefa_id):
    
    if not Tarefa.objects.filter(id=tarefa_id, usuario=request.user).exists():
        tarefa_id = get_valid_task_id(request.user)  # Obtém um novo ID válido
    
    if not tarefa_id:  # Se ainda não houver um ID válido, redireciona para a lista de tarefas
        return HttpResponseRedirect("/tarefas/") 
    
    tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)

    if request.method == "POST":
        tarefa.delete()
        return redirect("lista_tarefas")

    return render(request, "tarefas/deletar.html", {
        "tarefa": tarefa,
        "status_opcoes": Status.choices
    })

