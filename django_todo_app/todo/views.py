from django.shortcuts import redirect, render
from django.core.exceptions import PermissionDenied
from .models import *
from .forms import *

def todo_home(request):
  context = {}

  if request.method == "GET":

    data = ToDo.objects.all()

    context = {
      'title': "To Do Page",
      'data': data
    }

    return render(request, 'todo/dashboard.html', context)

  else:
    raise PermissionDenied

def add_todo(request):
  context = {}
  
  if request.method == 'GET':

    form = ToDoForm()

    context = {
      'title': "Add To Do",
      'form': form
    }

    return render(request, 'todo/form.html', context)

  else:
    form = ToDoForm(request.POST)

    if form.is_valid():
      form.save()
    else:
      print(form.errors.as_json())

    return redirect('home')

def view_todo(request,id):
  context = {}
  data = ToDo.objects.get(id = id)
  
  if request.method == 'GET':

    form = ToDoForm(instance = data)

    context = {
      'title': "View/Edit To Do",
      'form': form,
      'edit': True,
      'id': id,
    }

    return render(request, 'todo/form.html', context)

  else:
    form = ToDoForm(request.POST, instance=data)

    if form.is_valid():
      form.save()
    else:
      print(form.errors.as_json())

    return redirect('home')

def delete_todo(request,id):
  
  if request.method == 'GET':
    data = ToDo.objects.get(id = id)
    data.delete()

    return redirect('home')

  else:
    raise PermissionDenied