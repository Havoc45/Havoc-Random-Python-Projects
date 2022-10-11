from rest_framework import serializers
from todo.models import *

class ToDoSerializers(serializers.ModelSerializer):
  class Meta:
    model = ToDo
    fields = '__all__'