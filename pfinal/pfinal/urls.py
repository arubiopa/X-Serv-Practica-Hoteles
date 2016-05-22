from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pfinal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^template/(?P<path>.*)$','django.views.static.serve',
    	{'document_root': settings.STATIC2_URL}),
    url(r'^login$', 'miapp.views.ingresar'),
    url(r'^logout$', 'miapp.views.cerrar'),
    url(r'^infoUsuario$', 'miapp.views.infoUsuario'),
    url(r'^alojamientos$', 'miapp.views.mostrarTodos'),
    url(r'^alojamientos/(\d+)$', 'miapp.views.mostrarAloj'),
    url(r'^addComment/(\d+)$', 'miapp.views.addComment'),
    url(r'^(.*)/xml$', 'miapp.views.mostrarUsuario'),
    url(r'^about$', 'miapp.views.about'),
    url(r'^$', 'miapp.views.index'),
    url(r'^(.*)$', "miapp.views.usuario"),
)
