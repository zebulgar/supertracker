from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pixel', views.pixel, name='pixel'),
    path('show_image', views.show_image, name='show_image'),
]