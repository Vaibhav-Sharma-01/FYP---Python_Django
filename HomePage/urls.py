from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [

    path('', views.home, name='home'),

    path('/index', views.index, name='index'),

    path('/widget', views.widgets, name='widgets'),

    path('/main', views.Main, name='main'),

    url('/index', TemplateView.as_view(template_name="home/index.html"),
        name='index'),

    url('/main', TemplateView.as_view(template_name="home/main.html"),
        name='main'),

    url('/widget', TemplateView.as_view(template_name="home/widgets.html"),
        name='widget'),

]
