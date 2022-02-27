from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [

    path('', views.home, name='home'),

    path('/cricket/index', views.index, name='index'),

    path('/cricket/widget', views.widgets, name='widgets'),

    path('/cricket/main', views.Main, name='main'),

    url('/cricket/index', TemplateView.as_view(template_name="home/cricket/index.html"),
        name='index'),

    url('/cricket/main', TemplateView.as_view(template_name="home/cricket/main.html"),
        name='main'),

    url('/cricket/widget', TemplateView.as_view(template_name="home/cricket/widgets.html"),
        name='widget'),

    path('/football/index', views.findex, name='findex'),

    path('/football/widget', views.widgets, name='fwidgets'),

    path('/football/main', views.Main, name='fmain'),

    url('/football/index', TemplateView.as_view(template_name="home/football/index.html"),
        name='findex'),

    url('/football/main', TemplateView.as_view(template_name="home/football/main.html"),
        name='fmain'),

    url('/football/widget', TemplateView.as_view(template_name="home/football/widgets.html"),
        name='fwidget'),

]
