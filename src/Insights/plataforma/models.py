from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

# Zona de Perfil

class Perfil(models.Model):
    genero = (
        ('F','Femenino'),
        ('M','Masculino'),
    )
    title = (
        ('CM','Candidato Maestro'),
        ('MF','Maestro Fide'),
        ('MI','Maestro Internacional'),
        ('GM','Gran Maestro'),
    ) 
    sexo = models.CharField(max_length=1,blank=True,choices=genero)
    titulo = models.CharField(max_length=2,blank=True,choices=title)
    url = models.CharField(max_length=100, blank=True, default=None)
    #profile
    country = models.CharField(max_length=5, null=True, blank=True, default=None)
    location = models.CharField(max_length=20, null=True, blank=True, default=None)
    bio = models.CharField(max_length=100, null=True, blank=True, default=None)
    firstName = models.CharField(max_length=20, null=True, blank=True, default=None)
    lastName = models.CharField(max_length=20, null=True, blank=True, default=None)
    rating = models.IntegerField(null=True, blank=True)
    cuidad = models.IntegerField(null=True, blank=True)
    
    #Historial
    rated = models.IntegerField(null=True, blank=True)
    n_draw = models.IntegerField(null=True, blank=True)
    n_loss = models.IntegerField(null=True, blank=True)
    n_win = models.IntegerField(null=True, blank=True)

    username = models.OneToOneField('auth.User', related_name="nick", on_delete=models.CASCADE)
    
    def __unicode__(self):
        return self.username
    
class Foto(models.Model):
    ruta = models.ImageField(
        upload_to ='../imagenes/Profiles/', height_field=None, width_field=None, max_length=100)
    
    username =models.OneToOneField(Perfil, related_name="picture", null=True, blank=True, on_delete=models.CASCADE)
    
    def __unicode__(self):
        return self.username
    
    
    
class Elo(models.Model):
    nombre = models.CharField(max_length=30, null=True, blank=True, default=None)
    games = models.IntegerField()
    rating = models.IntegerField()
    rd = models.IntegerField()
    prog = models.IntegerField()
    
    username = models.ForeignKey(Perfil, related_name="rankings", null=True, blank=True, on_delete=models.CASCADE)
    
    def __unicode__(self):
        return self.username