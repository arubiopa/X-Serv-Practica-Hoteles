"""practicafinal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from pfinal import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^templates/(<?path>.*)$','django.views.static.serve',
        {'document_root':settings.STATIC_URL2}),
    url(r'update$', views.inicio),
    url(r'^login$', auth_views.login),
    url(r'^logout$', auth_views.logout),
    url(r'^alojamientos$', views.mostrarTodos),
    url(r'^alojamientos/(\d+)$', views.mostrarAloj),
    url(r'^(.*)/xml$', views.mostrarUsuario),
    url(r'^about$', views.about),
    url(r'^$', views.index),
]
