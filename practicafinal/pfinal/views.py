from django.shortcuts import render
from django.http import HttpResponse
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from xmlparser import myContentHandler
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
    lista = []
    lista = parse('es')
    respuesta =""
    for elem in lista:
        respuesta += str(elem) +"\n"
    return HttpResponse(respuesta)
