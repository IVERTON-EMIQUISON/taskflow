from django.contrib import admin  
from .models import Tarefa, Categoria, Arquivamento 

class TarefaAdmin(admin.ModelAdmin):  
    list_display = ('titulo', 'usuario', 'prazo', 'prioridade', 'concluida')  
    list_filter = ('prioridade', 'concluida', 'usuario')  
    search_fields = ('titulo', 'descricao')  
    date_hierarchy = 'prazo'  

admin.site.register(Categoria)  
admin.site.register(Tarefa, TarefaAdmin)  
admin.site.register(Arquivamento)


