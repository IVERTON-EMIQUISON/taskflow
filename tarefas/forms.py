from django import forms  
from .models import Tarefa, Categoria  

class TarefaForm(forms.ModelForm):  
    class Meta:  
        model = Tarefa  
        fields = ['titulo','descricao','categoria','status','prazo']  
        widgets = {  
            'prazo': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  
        }  
class CategoriaForm(forms.ModelForm):  # Adicionando o CategoriaForm
    class Meta:
        model = Categoria
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite a categoria de sua preferência'}),
        }