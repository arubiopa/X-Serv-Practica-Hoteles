from django.db import models

class Hotel (models.Model):
    nombre = models.CharField(max_length = 200)
    address = models.CharField(max_length = 200)
    phone = models.CharField(max_length = 200)
    body = models.TextField(max_length = 600)
    web = models.URLField()
    cat = models.TextField(max_length =32)
    subcat = models.TextField(max_length =32)
    nComentario = models.IntegerField()

class Imagen(models.Model):
    hotelId = models.IntegerField()
    url = models.URLField()

class Comentario(models.Model):
    comentario = models.TextField(max_length = 300)
    hotelId = models.IntegerField()
    fecha= models.DateField()

class HotelSeleccionado(models.Model):
    hotelId = models.IntegerField()
    usuario = models.CharField(max_length = 32)
    fecha = models.DateField()

class PagCSS(models.Model):
    usuario = models.CharField(max_length = 32)
    titulo = models.CharField(max_length = 32)
    colorFondo = models.TextField()
    tamano=models.IntegerField()
