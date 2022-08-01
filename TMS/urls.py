"""TMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from Main.views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('',view=base),
    path('Main/',include('Main.urls')),
    #path('tas',include('Main.urls')),
     path('',base, name='base'),
    path('tas',tas, name='tas'),
    path('talogin',talogin, name='talogin'),
    path('talogout',talogout,name='talogout'),
    path('facultylogin',facultylogin, name='facultylogin'),
    path('facultysignup',facultysignup, name='facultysignup'),
    path('studentlogin',studentlogin,name='studentlogin'),
    path('adminlogin',adminlogin, name='adminlogin'),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
