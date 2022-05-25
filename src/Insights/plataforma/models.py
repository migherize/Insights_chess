from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

# Data Science
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

class DataAnalyst(models.Model):
    games = models.CharField(max_length=20, null=True, blank=True, default=None)
    # cantidad
    win_w = models.IntegerField()
    draw_w = models.IntegerField()
    lose_w = models.IntegerField()
    win_b = models.IntegerField()
    draw_b = models.IntegerField()
    lose_b = models.IntegerField()

    opening = models.OneToOneField(opening, related_name="opening", on_delete=models.CASCADE)

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
    opening = models.CharField(max_length=20, null=True, blank=True, default=None)
    scienc = models.OneToOneField(DataAnalyst, related_name="scienc", on_delete=models.CASCADE)

class Moves(models.Model):
    white = models.CharField(max_length=255, null=True, blank=True, default=None)
    black = models.CharField(max_length=255, null=True, blank=True, default=None)
    result = models.CharField(max_length=20, null=True, blank=True, default=None)

class Games(models.Model):
    header_game = models.CharField(max_length=255, null=True, blank=True, default=None)
    move_game = models.CharField(max_length=255, null=True, blank=True, default=None)
    header = models.OneToOneField(Header, related_name="header", on_delete=models.CASCADE)
    moves = models.OneToOneField(Moves, related_name="moves", on_delete=models.CASCADE)

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
    
    #Historial
    rated = models.IntegerField(null=True, blank=True)
    n_draw = models.IntegerField(null=True, blank=True)
    n_loss = models.IntegerField(null=True, blank=True)
    n_win = models.IntegerField(null=True, blank=True)

    username = models.OneToOneField('auth.User', related_name="nick", on_delete=models.CASCADE)
    num_game = models.ForeignKey(Games, null=True, blank=True, on_delete=models.CASCADE)
    
    def __unicode__(self):
        return self.username


class Foto(models.Model):
    ruta = models.ImageField(
        upload_to ='../imagenes/Profiles/', height_field=None, width_field=None, max_length=100)
    
    picture =models.OneToOneField(Perfil, related_name="picture", null=True, blank=True, on_delete=models.CASCADE)
    
    def __unicode__(self):
        return self.picture
    
class Elo(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True, default=None)
    games = models.IntegerField()
    rating = models.IntegerField()
    rd = models.IntegerField()
    prog = models.IntegerField()
    
    ranking = models.ForeignKey(Perfil, related_name="rankings", null=True, blank=True, on_delete=models.CASCADE)
    
    def __unicode__(self):
        return self.ranking

