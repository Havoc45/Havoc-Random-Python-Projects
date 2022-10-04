from tabnanny import verbose
from django.db import models

class Switch(models.Model):
  switch = models.CharField( verbose_name  = 'Switch', max_length=256, null=True, blank=True)
  status = models.BooleanField(verbose_name  = 'Switch Status', default=False)
  timestamp = models.CharField(verbose_name  = 'Time Stamp', max_length=256, null=True, blank=True)
  
class SwitchArray(models.Model):
  switcharray = models.CharField( verbose_name  = 'Switch Array', max_length=256, null=True, blank=True)