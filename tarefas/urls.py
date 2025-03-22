from django.urls import path  
from . import views  
from .views import lista_tarefas, criar_tarefa, editar_tarefa, deletar_tarefa, buscar_tarefa_por_titulo, criar_categoria, excluir_categoria


urlpatterns = [  
    path('', views.lista_tarefas, name='lista_tarefas'),  
    path('criar/', views.criar_tarefa, name='criar_tarefa'),  
    path("excluir_categoria/", views.excluir_categoria, name="excluir_categoria"),

    path("deletar/<int:tarefa_id>/", deletar_tarefa, name="deletar_tarefa"),
    path('tarefas/<int:pk>/status/', views.atualizar_status, name='atualizar_status'),  
    path("editar/<int:id>/", editar_tarefa, name="editar_tarefa"),
    path("buscar_tarefa_por_titulo/", buscar_tarefa_por_titulo, name="buscar_tarefa_por_titulo"),

]  