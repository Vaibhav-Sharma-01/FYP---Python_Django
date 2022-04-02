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

    re_path('/football/index', TemplateView.as_view(template_name="home/football/index.html"),
            name='findex'),

    path('/basketball/index', views.bindex, name='bindex'),

    re_path('/basketball/index', TemplateView.as_view(template_name="home/basketball/index.html"),
            name='bindex'),

    re_path('/games/home', TemplateView.as_view(template_name="home/games/home.html"),
            name='home'),

    path('/games/trivia', views.triviaindex, name='triviaindex'),

    re_path('/games/trivia', TemplateView.as_view(template_name="home/games/trivia.html"),
            name='trivia'),

    path('/games/index', views.bball, name='bballindex'),

    re_path('/games/index', TemplateView.as_view(template_name="home/games/index.html"),
            name='BasketBallGame'),

    path('/games/chess', views.chess, name='chessindex'),

    re_path('/games/chess', TemplateView.as_view(template_name="home/games/chess.html"),
            name='chess'),

]
