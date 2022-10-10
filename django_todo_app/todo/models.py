from django.db import models
from datetime import datetime

class ToDo(models.Model):
  title  = models.CharField(verbose_name  = 'Title', max_length=256, null=True, blank=True)
  description = models.CharField(verbose_name  = 'Description', max_length=256, null=True, blank=True)
  modified_at = models.DateTimeField(verbose_name = 'Last Mdified At', auto_now=True, auto_now_add=False)
  created_at  = models.DateTimeField(verbose_name = 'Created At', auto_now=False, auto_now_add=True)
