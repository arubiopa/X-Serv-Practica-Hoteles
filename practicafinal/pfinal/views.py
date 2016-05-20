from django.shortcuts import render
from django.http import HttpResponse
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from xmlparser import myContentHandler
from models import Hotel,Imagen,Comentario,HotelSeleccionado,PagCSS
from django.template.loader import get_template
from django.template import Context
import urllib2
import sys
import os.path

# Create your views here.
def parse(idioma):
    print("COMIEZA EL PARSEO")
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    if idioma =='es':
        xmlfile = urllib2.urlopen("http://cursosweb.github.io/etc/alojamientos_es.xml")
    theParser.parse(xmlfile)
    lista = theHandler.veolista()
    print "parse" + idioma
    return lista

def inicio(request):
    lista = {}
    lista = parse('es')
    respuesta =""
    for elem in lista:
        #print ("prueba" + elem["name"])
        try:
            elem["subcat"]
        except Exception as e:
            elem["subcat"] = "Undefined"

        object_hotel = Hotel(nombre=elem["name"],address=elem['address'],
                    phone=elem['phone'],body=elem['body'],web=elem['web'],
                        cat=elem['cat'],subcat=elem["subcat"])
        object_hotel.save()

        idHotel = object_hotel.id
        for url in elem["url"]:
            objectImagen = Imagen(hotelId=idHotel,url=url)
            objectImagen.save()


    return HttpResponse(respuesta)

def loggin(request, recurso):
    hoteles = Hotel.objects.all()
    usuarios = PagCSS.objects.all()
    if request.user.is_authenticated():
        try:
            usuario = PagCSS.objets.get(usuario = request.user.username)
        except PagCSS.DoesNotExit:
            c = context({'hoteles':hoteles,})
    else:
        return 'Estas registrado como: <a href="/'+ request.user.username +'">' + request.user.username + '</a> <br><a href="/logout">logout</a>'

def mostrarUsuario(request):
    respuesta = ""
    return HttpResponse(respuesta)

def mostrarTodos(request):
    respuesta = ""
    return HttpResponse(respuesta)

def mostrarAloj(request,id):
    respuesta = "respuesta: "
    return HttpResponse(respuesta + id)

def mostrarCss(request):
    respuesta = ""
    return HttpResponse(respuesta)

def index(request):
    template = get_template("index.html")
    estado="no estas logueado"
    if(request.user.is_authenticated()):
        estado = "estado logueado"
    c = Context({"estado":estado})
    renderizado = template.render(c)
    return HttpResponse(renderizado)

def about(request):
    respuesta = ""
    return HttpResponse(respuesta)
