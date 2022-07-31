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
    titulo = (
        ('CM','Candidato Maestro'),
        ('MF','Maestro Fide'),
        ('MI','Maestro Internacional'),
        ('GM','Gran Maestro'),
    ) 
    sex = models.CharField(max_length=1,blank=True,choices=genero)
    title = models.CharField(max_length=2,blank=True,choices=titulo)
    url = models.CharField(max_length=100, blank=True, default=None)
    #profile
    country = models.CharField(max_length=5, null=True, blank=True, default=None)
    city = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=20, null=True, blank=True, default=None)
    biography = models.CharField(max_length=100, null=True, blank=True, default=None)
    firstName = models.CharField(max_length=20, null=True, blank=True, default=None)
    lastName = models.CharField(max_length=20, null=True, blank=True, default=None)
    rating = models.IntegerField(null=True, blank=True)
    kind = models.IntegerField(null=True, blank=True)
    
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
    
    perfil = models.OneToOneField(Perfil, related_name="perfil", null=True, blank=True, on_delete=models.CASCADE)
    
    def __unicode__(self):
        return self.picture
    
class Elo(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True, default=None)
    games = models.IntegerField()
    rating = models.IntegerField()
    rd = models.IntegerField()
    prog = models.IntegerField()
    
    perfil = models.ForeignKey(Perfil, related_name="rankings", null=True, blank=True, on_delete=models.CASCADE)
    
    def __unicode__(self):
        return self.ranking

class Games(models.Model):
    header_game = models.TextField(null=True, blank=True, default=None)
    move_game = models.TextField(null=True, blank=True, default=None)
    perfil = models.ForeignKey(Perfil, related_name="partidas", null=True, blank=True, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.id_perfil

# Data Science

class DataAnalyst(models.Model):
    games = models.CharField(max_length=20, null=True, blank=True, default=None)
    # cantidad
    win_w = models.IntegerField()
    draw_w = models.IntegerField()
    lose_w = models.IntegerField()
    win_b = models.IntegerField()
    draw_b = models.IntegerField()
    lose_b = models.IntegerField()

class opening(models.Model):
    # ecos frecuencia high
    eco_ww = models.CharField(max_length=20, null=True, blank=True, default=None)
    eco_dw = models.CharField(max_length=20, null=True, blank=True, default=None)
    eco_lw = models.CharField(max_length=20, null=True, blank=True, default=None)
    eco_b = models.CharField(max_length=20, null=True, blank=True, default=None)
    eco_db = models.CharField(max_length=20, null=True, blank=True, default=None)
    eco_lb = models.CharField(max_length=20, null=True, blank=True, default=None)
    # ecos frecuencia high
    n_eco_ww = models.IntegerField()
    n_eco_dw = models.IntegerField()
    n_eco_lw = models.IntegerField()
    n_eco_b = models.IntegerField()
    n_eco_db = models.IntegerField()
    n_eco_lb = models.IntegerField()

    data = models.OneToOneField(DataAnalyst, related_name="data_ciencia", on_delete=models.CASCADE)

class Header(models.Model):
    event = models.CharField(max_length=20, null=True, blank=True, default=None)
    site = models.CharField(max_length=20, null=True, blank=True, default=None)
    date = models.CharField(max_length=20, null=True, blank=True, default=None)
    white = models.CharField(max_length=20, null=True, blank=True, default=None)
    elo_w = models.CharField(max_length=20, null=True, blank=True, default=None)
    elo_b = models.CharField(max_length=20, null=True, blank=True, default=None)
    black = models.CharField(max_length=20, null=True, blank=True, default=None)
    result = models.CharField(max_length=20, null=True, blank=True, default=None)
    variant = models.CharField(max_length=20, null=True, blank=True, default=None)
    eco = models.CharField(max_length=20, null=True, blank=True, default=None)
    opening = models.CharField(max_length=250, null=True, blank=True, default=None)
    
    game = models.OneToOneField(Games, related_name="header", on_delete=models.CASCADE)
    scienc = models.ForeignKey(DataAnalyst, related_name="data_analisis", null=True, blank=True, on_delete=models.CASCADE)


class Moves(models.Model):
    white = models.TextField(null=True, blank=True, default=None)
    black = models.TextField(null=True, blank=True, default=None)
    result = models.CharField(max_length=20, null=True, blank=True, default=None)
    game = models.OneToOneField(Games, related_name="moves", on_delete=models.CASCADE)
