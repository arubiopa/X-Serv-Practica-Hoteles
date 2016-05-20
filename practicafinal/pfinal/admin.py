from django.contrib import admin

from models import Hotel,Imagen,Comentario,HotelSeleccionado,PagCSS
# Register your models here.
admin.site.register(Hotel)
admin.site.register(Imagen)
admin.site.register(Comentario)
admin.site.register(HotelSeleccionado)
admin.site.register(PagCSS)
