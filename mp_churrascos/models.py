from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class MpTopic(models.Model):
    """Um assunto do Usuário"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'MpTopics'

    def __str__(self) -> str:
        """Delvolve text"""
        return self.text
    
class MpEntry(models.Model):
    """Uma entrada do Usuário"""
    topic = models.ForeignKey(MpTopic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'MpEntries'

    def __str__(self) -> str:
        """Delvolve text"""
        return self.text[:50] + '...'
    
class MpUsuarioChurrasco(models.Model):
    """Um Usuário Churrasco"""
    cpf = models.CharField(max_length=14)
    cep = models.CharField(max_length=9)
    qtdPessoas = models.CharField(max_length=4)
    resultado = models.CharField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)
    endereco = models.CharField(max_length=200)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    distancia = models.CharField(max_length=10)
    tipoTransporte = models.CharField(max_length=20)
    kitBebidas = models.CharField(max_length=200)
    kitCarnes = models.CharField(max_length=200)
