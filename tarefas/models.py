from django.db import models  
from django.contrib.auth.models import User  
from django.utils import timezone  

class Categoria(models.Model):  
    nome = models.CharField(max_length=50)  
    
    def __str__(self):  
        return self.nome  

class Status(models.TextChoices):  
    PENDENTE = "Pendente", "Pendente"  
    PLANEJADA = "Planejada", "Planejada"  
    EM_ANDAMENTO = "Em andamento", "Em andamento"  
    AGUARDANDO_APROVACAO = "Aguardando aprovação", "Aguardando aprovação"  
    CONCLUIDA = "Concluída", "Concluída"  

class Arquivamento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tarefa = models.ForeignKey('Tarefa', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CONCLUIDA)
    arquivada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tarefa.titulo} - {self.status}"


class Tarefa(models.Model):  
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  
    titulo = models.CharField(max_length=200)  
    descricao = models.TextField(blank=True, null=True)  
    prazo = models.DateTimeField(null=False)   
    prioridade = models.CharField(max_length=10, choices=[  
        ('Baixa', 'Baixa'),  
        ('Média', 'Média'),  
        ('Alta', 'Alta')  
    ])  
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)  
    concluida = models.BooleanField(default=False)  
    status = models.CharField(  
        max_length=20,  
        choices=Status.choices,  # Correção: Referência correta às opções de status  
        default=Status.PENDENTE  # Ajuste para um valor padrão válido  
    )  
    
    criada_em = models.DateTimeField(auto_now_add=True)  

    def __str__(self):  
        return self.titulo  

    def atrasada(self):  
        return not self.concluida and self.prazo < timezone.now()  # Use timezone.now()  
    def concluir_tarefa(self):  
        """ Marca a tarefa como concluída e arquiva automaticamente se o status for 'Concluída'. """  
        if self.status == Status.CONCLUIDA and not self.concluida:  
            self.concluida = True  
            self.status = Status.CONCLUIDA  # Usando a enumeração Status  
            self.save()  

            # Agora, vamos criar o arquivamento  
            Arquivamento.objects.create(usuario=self.usuario, tarefa=self)  
        else:  
            # Se a tarefa já está concluída, talvez você queira lançar uma exceção ou apenas ignorar  
            print("A tarefa já está concluída ou o status não é 'Concluída'.")  

