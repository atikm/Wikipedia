from django.urls import path

from . import views
import encyclopedia
app_name:encyclopedia
urlpatterns = [
    path("", views.index, name="index"),
    path("?q=" , views.get_search , name="wiki_search"),
    path("random" , views.get_random_entry, name="random_page"),
    path("creat" , views.create_page , name="create_page"),
    path("edit?title=" , views.edit_page , name="editpage"),
    path("wiki/<str:title>" , views.get_page , name="wiki")
    
]
