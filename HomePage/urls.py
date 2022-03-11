from django.urls import re_path
from django.contrib import admin
from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [

    path('', views.home, name='home'),

    path('/cricket/index', views.index, name='index'),

    path('/cricket/widget', views.widgets, name='widgets'),

    path('/cricket/main', views.Main, name='main'),

    re_path('/cricket/index', TemplateView.as_view(template_name="home/cricket/index.html"),
            name='index'),

    re_path('/cricket/main', TemplateView.as_view(template_name="home/cricket/main.html"),
            name='main'),

    re_path('/cricket/widget', TemplateView.as_view(template_name="home/cricket/widgets.html"),
            name='widget'),

    path('/football/index', views.findex, name='findex'),

    path('/football/widget', views.widgets, name='fwidgets'),

    path('/football/main', views.Main, name='fmain'),

    re_path('/football/index', TemplateView.as_view(template_name="home/football/index.html"),
            name='findex'),

    re_path('/football/main', TemplateView.as_view(template_name="home/football/main.html"),
            name='fmain'),

    re_path('/football/widget', TemplateView.as_view(template_name="home/football/widgets.html"),
            name='fwidget'),

    path('/basketball/index', views.bindex, name='bindex'),

    path('/basketball/main', views.Main, name='bmain'),

    path('/basketball/widget', views.widgets, name='bwidgets'),

    re_path('/basketball/index', TemplateView.as_view(template_name="home/basketball/index.html"),
            name='bindex'),

    re_path('/basketball/main', TemplateView.as_view(template_name="home/basketball/main.html"),
            name='bmain'),

    re_path('/basketball/widget', TemplateView.as_view(template_name="home/basketball/widgets.html"),
            name='bwidget'),

]
