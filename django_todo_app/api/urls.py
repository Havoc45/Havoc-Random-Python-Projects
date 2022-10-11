from django.urls import path
from .views import *

urlpatterns = [
  path('get_todo/', getToDo),
  path('add_todo/', addToDo),
  path('view_todo/<int:id>/',viewToDo),
  path('delete_todo/<int:id>/',deleteToDo),
]