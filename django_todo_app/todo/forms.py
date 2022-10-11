from socket import fromshare
from django import forms 
from .models import *

class ToDoForm(forms.ModelForm):

  title =  forms.CharField( label = ('Title'),required=True, widget=forms.TextInput(
		attrs= {
		# 'disabled':'',
        }
    ))

  description = forms.CharField( label = ('Description'),required=False, widget=forms.Textarea(
		attrs= {
		# 'disabled':'',
        }
    ))
    
  class Meta:
      model = ToDo
      fields = ("title","description",)
