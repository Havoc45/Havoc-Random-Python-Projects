from django.urls import path
from .views import *

urlpatterns = [

   path('', todo_home,name = 'home'),
   path('add/', add_todo, name = 'add'),
   path('view/<int:id>', view_todo, name = 'view'),
   path('delete/<int:id>/',delete_todo, name = 'delete'),
]