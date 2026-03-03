from django.db import models

# Create your models here.

class Chat_sessions(models.Model): 
    id_sesion = models.AutoField(primary_key=True)
    fecha_inicio = models.DateTimeField(auto_now_add=True)



class Chat_session(models.Model): 
    class RoleChoices(models.TextChoices):
        USUARIO = 'user', 'Usuario'
        IA = 'ia', 'asistente'
    id_mensaje = models.AutoField(primary_key=True)
    id_sesion = models.ForeignKey(Chat_sessions, on_delete=models.CASCADE)
    
    role = models.CharField(
        max_length=10, 
        choices= RoleChoices.choices,
        default=RoleChoices.USUARIO
    )
    contenido = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta: 
        ordering = ['timestamp']

    def __str__(self): 
        return f"{self.role}: {self.contenido[:50]}..."        