from django.urls import path

from . import views

app_name = 'game'

urlpatterns = [
    path('get_leaf', views.get_leaf_node, name='get_leaf'),
    path('get-leaf', views.get_leaf_node, name='get-leaf'),
    path('', views.index, name='index'),
]