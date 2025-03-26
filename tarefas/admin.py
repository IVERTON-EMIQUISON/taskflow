from django.contrib import admin  
from .models import Tarefa, Categoria, Arquivamento 

class TarefaAdmin(admin.ModelAdmin):  
    list_display = ('titulo', 'usuario', 'prazo', 'prioridade', 'concluida')  
    list_filter = ('prioridade', 'concluida', 'usuario')  
    search_fields = ('titulo', 'descricao')  
    date_hierarchy = 'prazo'  

class ArquivamentoAdmin(admin.ModelAdmin):
    list_display = ('tarefa', 'usuario', 'status', 'arquivada_em')
    list_filter = ('status', 'arquivada_em')
    search_fields = ('tarefa__titulo', 'usuario__username')
    actions = ['remover_tarefas_concluidas']

    def remover_tarefas_concluidas(self, request, queryset):
        """Ação personalizada para excluir tarefas arquivadas"""
        tarefas_removidas = queryset.delete()
        self.message_user(request, f"{tarefas_removidas[0]} tarefas concluídas removidas.")
    
    remover_tarefas_concluidas.short_description = "Remover tarefas concluídas"

admin.site.register(Arquivamento, ArquivamentoAdmin)
admin.site.register(Categoria)  
admin.site.register(Tarefa, TarefaAdmin)  
