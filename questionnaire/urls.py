from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^respond/', views.respond, name='respond'),
    url(r'^about/', views.about, name='about'),
]
