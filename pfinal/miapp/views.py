from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound,HttpResponseRedirect
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from xmlparser import myContentHandler
from models import Hotel,Imagen,Comentario,HotelSeleccionado,PagCSS
from django.template.loader import get_template
from django.contrib.auth import login, authenticate, logout
from django.template import Context
from datetime import *
import urllib2
import sys
import os.path
longitud =10
# Create your views here.
def parse(idioma):
    print("COMIEZA EL PARSEO")
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    if idioma =='es':
        xmlfile = urllib2.urlopen("http://cursosweb.github.io/etc/alojamientos_es.xml")
    if idioma =='en':
        xmlfile = urllib2.urlopen("http://cursosweb.github.io/etc/alojamientos_en.xml")
    if idioma =='fr':
        xmlfile = urllib2.urlopen("http://cursosweb.github.io/etc/alojamientos_fr.xml")
    theParser.parse(xmlfile)
    lista = theHandler.veolista()
    print "parse" + idioma
    return lista


def formatearCSS(request):
    if request.user.is_authenticated():
        try:
            page = PagCSS.objects.get(usuario = request.user.username)
        except Exception as e:
            return ""

        background = page.colorFondo
        letra = page.tamano
        salida = "body{background:"+background+"}"
        salida+="*{font-size:"+str(letra)+"px}"
        return salida
    else:
        return ""


def comprobacionUser(request):
    if  request.user.is_authenticated():
        try:
            us = PagCSS.objects.get(usuario = request.user.username)
        except PagCSS.DoesNotExist:
            us = PagCSS(usuario =request.user.username,titulo = "Pagina personal de " + request.user.username,colorFondo = "url(images/bg-body.png) repeat-x top center #E8F7F9;",tamano=12)
            us.save()

def inicio(request):
    global longitud
    longitud =10
    hoteles = Hotel.objects.all()
    if(len(hoteles) == 0):
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
                            cat=elem['cat'],subcat=elem["subcat"],nComentario=0)
            object_hotel.save()

            idHotel = object_hotel.id
            for url in elem["url"]:
                objectImagen = Imagen(hotelId=idHotel,url=url)
                objectImagen.save()

def ingresar(request):
    global longitud
    longitud =10
    if request.method == "POST":
        user = request.POST['Username']
        passw = request.POST['Password']
        acceso = authenticate(username = user,password = passw)
        if acceso is not None:
            if acceso.is_active:
                login(request,acceso)
                comprobacionUser(request)
                return HttpResponseRedirect('/'+user)
            else:
                return HttpResponseNotFound ( "usuario no activo")
        else:
            return HttpResponseNotFound ( "usuario no valido")

def cerrar(request):
    global longitud
    longitud =10
    logout(request)
    return HttpResponseRedirect('/')


def formulariolog(request):
    if not request.user.is_authenticated():
        return '<form method="post" action="/login"><table><td><input type="text"name="Username" Username=""</td>'+\
                     '</tr><td><input type="password"name="Password" Password=""</td></tr></table><input type="submit" value="login" /></form></br>'
    else:
        return 'Estas logueado como: <a href="/'+ request.user.username +'">' + request.user.username + '</a> <br><a href="/logout">logout</a></br>'


def mostrarUsuario(request,usuario):
    global longitud
    longitud =10
    hoteles = HotelSeleccionado.objects.all()
    hoteles = hoteles.filter(usuario=usuario)
    xml = "<?xml version='1.0' encoding='UTF-8' ?>"
    xml += "<data><usuario name='" + usuario +"'>"
    for ho in hoteles:
        hotel = Hotel.objects.get(id=ho.hotelId)
        xml+="<hotel>"
        xml+="<nombre>" +hotel.nombre+"</nombre>"
        xml+="<address>" +hotel.address+"</address>"
        xml+="<phone>" +hotel.phone+"</phone>"
        xml+="<web>" +hotel.web+"</web>"
        xml+="<cat>" +hotel.cat+"</cat>"
        xml+="<subcat>" +hotel.subcat+"</subcat></hotel>"

    xml+="</usuario></data>"
    return HttpResponse(xml,content_type="text/xml")

def filtroForm():
    return( '<form method="post">Filtre:<select name="Filtro">'+
        '<option value="Categoria">Categoria</option> ' +
        '<option value="SubCategoria">SubCategoria</option> ' +
        '</select> <input type="text"name="valor" value="" /><button type="submit"> Enviar</button> </form>')

def mostrarTodos(request):
    global longitud
    longitud =10
    hoteles = Hotel.objects.all()

    if request.method == "POST":
        atributo = request.POST['Filtro']
        filtro =  request.POST['valor']
        if(atributo=="Categoria"):
            hoteles = hoteles.filter(cat=filtro)
        else:
            hoteles = hoteles.filter(subcat=filtro)

    html="<p>Numero de resultados: " + str(len(hoteles)) + "</p<ul>"
    for ho in hoteles:
        html += "<li><a href='alojamientos/" + str(ho.id) + "'>"+ho.nombre+ "</a></li>"
    html+="</ul>"
    template = get_template("todos.html")
    c = Context({"css":formatearCSS(request),"form":filtroForm(),"hoteles":html,"log":formulariolog(request),"infoUsuarios":infoUsuarios(request)})

    renderizado = template.render(c)
    return HttpResponse(renderizado)

def ComentarioHoteles(id):
    comentarios = Comentario.objects.all()
    comentarios = comentarios.filter(hotelId=id)
    salida=""
    if(len(comentarios)!=0):
        for c in comentarios:
            salida += "<p>--> Fecha: "+ str(c.fecha)
            salida +=  "  "+ c.comentario +"</p>"
    else:
        return ("<p> HOTEL SIN COMENTARIOS</p>")
    return salida

def botonesIdioma(request,id):
    if request.user.is_authenticated():
        html = '<form method="POST" action=/alojamientos/'+ str(id)+'><button type="submit" value="EN" name="EN">EN</button>'
        html += '<button type="submit" value="FR" name="FR">FR</button>'
        html+= '<button type="submit" value="ADD" name="ADD">Agregar a mi coleccion</button></form>'
        return html

    else:
        return ""
def addComment(request,id):
    global longitud
    longitud =10
    ho = Hotel.objects.get(id=id)
    if (request.method == "POST") :
        if len(request.POST['coment']) != 0:
            comentario = request.POST['coment']

        ho.nComentario = ho.nComentario + 1
        ho.save()

        object_comentario = Comentario(comentario=comentario,hotelId=ho.id,fecha=datetime.now())
        object_comentario.save()
        return HttpResponseRedirect('/alojamientos/' + str(ho.id) )


def mostrarAloj(request,id):
    global longitud
    longitud =10
    salida = ""
    ho = Hotel.objects.get(id=id)
    encontrado = 0
    if (request.method == "POST") :
        try:
            request.POST["ADD"]
        except Exception as e:
            try:
                request.POST["EN"]
            except Exception as e:
                print ("FRANCES")
                lista = parse("fr")

            try:
                request.POST["FR"]
            except Exception as e:
                print ("INGLES")
                lista = parse("en")

            for elem in lista:
                if(elem["name"] == ho.nombre):
                    salida += "<h3>" + elem["name"] + "</h3>"
                    salida += "<ul><li>" +elem["address"] + elem["phone"] + "</li>"
                    salida += "<li>" + elem["cat"] + elem["subcat"] + "</li>"
                    salida += "<li>" + elem["web"] + "</li>"
                    if len(elem["body"]) != 0:
                        salida += "<li>" + elem["body"] + "</li></ul>"
                    encontrado =1
                    break
        else:
            encontrado =1
            hotel = HotelSeleccionado(hotelId=ho.id,usuario=request.user.username,fecha=datetime.now())
            hotel.save()

        if encontrado == 0:
            salida += "<h3> ESTE HOTEL NO SE ENCUENTRA EN ESTE IDIOMA</h3></br></br>"

    salida += "<h3>" + ho.nombre + "</h3>"
    salida += "<ul><li>" + ho.address + ho.phone + "</li>"
    salida += "<li>" + ho.cat + ho.subcat + "</li>"
    salida += "<li>" + ho.web + "</li>"

    if len(ho.body) != 0:
        salida += "<li>" + ho.body + "</li></ul>"

    imagen = Imagen.objects.all()
    imagen = imagen.filter(hotelId=ho.id)
    for i in imagen:
        salida += "<img class='imagenes' src='" + i.url + "'>"

    template = get_template("alojamientoid.html")

    c = Context({"css":formatearCSS(request),"botones":botonesIdioma(request,ho.id),"form":formComent(request,ho.id),"log":formulariolog(request),"hoteles":salida,"infoUsuarios":infoUsuarios(request),"nombre":ho.nombre,"comentarios":ComentarioHoteles(ho.id)})
    renderizado = template.render(c)
    return HttpResponse(renderizado)


def infoUsuarios(request):
    usuarios = PagCSS.objects.all()
    salida = ""
    for usuario in usuarios:
        salida += '<a href="/'+ usuario.usuario +'">' + usuario.usuario + '</a></br>'
        salida += 'Titulo: ' + usuario.titulo + "</br>"
    return salida

def hotelesSeleccionados(request,usuario):
    global longitud
    if request.method == "POST":
        longitud += 10

    hoteles = HotelSeleccionado.objects.all()
    html ="<ul>"
    i=0
    hoteles = hoteles.filter(usuario=usuario)
    if(len(hoteles)==0):
        return ("<p> Ningun Hotel selecionado por el usuario</p>")

    for hotel in hoteles:
        imagen = Imagen.objects.all()
        imagen = imagen.filter(hotelId=hotel.hotelId)
        ho = Hotel.objects.get(id=hotel.hotelId)
        html += "<li>"+  ho.nombre + " Direccion: " + ho.address
        if (len(imagen) != 0):
            html+= "<img class='imagenesPeques' src='" + imagen[0].url + "'></br>"
        html +=  "Fecha: "+ str(hotel.fecha) +"<a href='alojamientos/" + str(ho.id) + "'> +Info</a></li>"

        i+=1
        if(i==longitud):
            html+="</ul>"
            break

    if(len(hoteles)>longitud):
        html += '<form method="post"  action=/' + usuario + '>' +'<button type="submit" > Siguiente</button></form>'
    return(html)


def infoUsuario(request):
    global longitud
    longitud =10
    nombre = request.user.username
    usuario = PagCSS.objects.get(usuario = nombre)

    if len(request.POST['titulo']) != 0:
        usuario.titulo = request.POST['titulo']
    if len(request.POST['fondo']) != 0:
        usuario.colorFondo = request.POST['fondo']
    if len(request.POST['letra']) != 0:
        usuario.tamano = request.POST['letra']
    usuario.save()
    return HttpResponseRedirect('/' + nombre)


def usuario(request,usuario):
    if request.method=="GET":
        global longitud
        longitud =10

    cambiar=""
    cambiarcss=""
    if(request.user.is_authenticated() and usuario == request.user.username):
        cambiar = ' <form method="post" action="/infoUsuario"><table>'
        cambiar += 'Titulo:<input type="text"name="titulo" titulo=""'
        cambiarcss = ' <form method="post" action="/cambiarcss"><table>Color fondo:'
        cambiarcss += '<input type="text"name="fondo" fondo=""></br>'
        cambiarcss += 'Letras:<input type="text"name="letra" letra=""></br><input type="submit" value="Enviar"/></form>'

    info = PagCSS.objects.get(usuario=usuario)
    template = get_template("paginausuario.html")
    c = Context({"css":formatearCSS(request),"form":cambiar,"formcss":cambiarcss,"titulo":info.titulo,"hoteles":hotelesSeleccionados(request,usuario),"log":formulariolog(request),"infoUsuarios":infoUsuarios(request)})
    renderizado = template.render(c)
    return HttpResponse(renderizado)

def index(request):
    global longitud
    longitud =10
    inicio(request)
    template = get_template("index.html")
    c = Context({"css":formatearCSS(request),"log":formulariolog(request),"hotelesHome":buscarComentarios(),"infoUsuarios":infoUsuarios(request)})
    renderizado = template.render(c)
    return HttpResponse(renderizado)


def formComent(request,idd):

    if request.user.is_authenticated():
         return ('<form  method="post" action="/addComment/' + str(idd) + '">Escriba comentario: <input type="text"name="coment" coment=""/><input type="submit" value="Enviar" /></form>')
    else:
        return ""

def  buscarComentarios():
    salida="<ul>"
    i=0;
    j=0
    arr=[]

    hoteles = Hotel.objects.all()
    hoteles = hoteles.order_by("-nComentario")

    for ho in hoteles:
        if(ho.nComentario > 0):
            imagen = Imagen.objects.all()
            imagen = imagen.filter(hotelId=ho.id)
            salida += "<li><a href='" + ho.web + "'>"+ho.nombre+ "</a> + Direccion: " + ho.address
            if (len(imagen) > 0):
                salida+="<img class='imagenesPeques' src='" + imagen[0].url + "'>"
            salida += "<a href='alojamientos/" + str(ho.id) + "'> +Info</a></li>"
            i+=1
            if(i==10):
                salida+="</ul>"
                return salida
        else:
            continue
    return salida

def about(request):
    global longitud
    longitud =10
    template = get_template("about.html")
    c=Context({"css":formatearCSS(request)})
    renderizado = template.render(c)
    return HttpResponse(renderizado)
