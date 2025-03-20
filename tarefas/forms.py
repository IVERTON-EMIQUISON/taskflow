from django import forms  
from .models import Tarefa  

class TarefaForm(forms.ModelForm):  
    class Meta:  
        model = Tarefa  
        fields = ['titulo','descricao','categoria','status' ]  
        widgets = {  
            'prazo': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  
        }  