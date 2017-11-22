
from django.conf.urls import url

from vacancies import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^show_json/', views.show_json, name='show_json'),
    url(r'^response/', views.response, name='response'),
]
