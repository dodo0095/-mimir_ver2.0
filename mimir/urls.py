"""mimir URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path,include
from base.views import hello_view,pos_table,neg_table,neg_fin_table,pos_fin_table
from crawler.views import crawler

urlpatterns = [
	path('admin/', admin.site.urls),
    path('',hello_view),
    path("pos_table/",pos_table),
    path("neg_table/",neg_table),
    path("neg_fin_table/",neg_fin_table),
    path("pos_fin_table/",pos_fin_table),
    path('crawler/',include('crawler.urls')),

]
