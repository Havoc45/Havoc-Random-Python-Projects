from rest_framework.decorators import api_view
from rest_framework.response import Response\

from .serializers import *
from todo.models import * 

@api_view(['GET'])
def getToDo(request):
  data = ToDo.objects.all()
  serializer = ToDoSerializers(data, many = True)
  return Response(serializer.data)

@api_view(['POST'])
def addToDo(request):
  serializer = ToDoSerializers(data = request.data)

  if serializer.is_valid():
    serializer.save()

  return Response({'action': 'Add To Do', 'status': 'success', 'message': 'To Do is Successfully Added!', 'data': serializer.data})


@api_view(['GET'])
def viewToDo(request,id):
  data = ToDo.objects.get(id = id)
  serializer = ToDoSerializers(data)
  return Response(serializer.data)

@api_view(['GET'])
def deleteToDo(request,id):
  data = ToDo.objects.get(id = id)
  data.delete()
  return Response({'action': 'Delete To Do', 'status': 'success', 'message': 'To Do is Successfully Deleted!'})