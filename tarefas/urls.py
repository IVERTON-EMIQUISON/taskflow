from django.urls import path  
from . import views  
from .views import lista_tarefas, criar_tarefa, editar_tarefa, deletar_tarefa, buscar_tarefa_por_titulo


urlpatterns = [  
    path('', views.lista_tarefas, name='lista_tarefas'),  
    path('criar/', views.criar_tarefa, name='criar_tarefa'),  
     
   # path('buscar_tarefa_por_titulo/<str:titulo>/', views.buscar_tarefa_por_titulo, name='buscar_tarefa_por_titulo'),
   # path('editar_tarefa/<int:id>', editar_tarefa, name='editar_tarefa'),
    path("deletar/<int:tarefa_id>/", deletar_tarefa, name="deletar_tarefa"),
    path('concluir/<int:id>/', views.concluir_tarefa, name='concluir_tarefa'),  
    path('tarefas/<int:pk>/status/', views.atualizar_status, name='atualizar_status'),  
    path("editar/<int:id>/", editar_tarefa, name="editar_tarefa"),
    path("buscar_tarefa_por_titulo/", buscar_tarefa_por_titulo, name="buscar_tarefa_por_titulo"),

]  