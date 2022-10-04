import json
from io import BytesIO
from sqlite3 import Timestamp
import pandas as pd
from operator import attrgetter
import datetime

from django.shortcuts import render
from nosairis_sensor_dashboard.settings import BASE_DIR
from django.http import FileResponse, Http404

import switch
from .models import *


def Home(request):
  if request.method == 'GET':

    switchArray = None

    if(SwitchArray.objects.all()):
      switchArray = (SwitchArray.objects.all())[0]

    context = {
        'title': 'Dashboard',
        'data': json.loads(switchArray.switcharray) if switchArray else None,
    }

    return render(request,'switch/dashboard.html',context)


def viewSwitch(request, switchname):
  if request.method == 'GET':

    if(switchname is not None):
      switchData = Switch.objects.filter(switch = switchname)
      data = []
      label = []
      
      for i,sd in enumerate(switchData):

        data.append({
          'status': (1 if sd.status else 0),
          'timestamp': int(sd.timestamp),
        })

        if i == 0 or i == len(switchData)-1:
          label.append(int(sd.timestamp))

      print(label)
      
      context = {
          'title': f'View Switch - {switchname}',
          'data': data,
          'label': label,
          'switch': switchname,
      }

      return render(request,'switch/viewgraph.html',context)  

    else:
      raise Http404

def reportPingLost(request):
  if request.method == 'GET':
    
    switchData = Switch.objects.filter(status = False)
    data = []
      
    for sd in switchData:
      temptimestamp = datetime.datetime.utcfromtimestamp(int(sd.timestamp)) 
      data.append({
        'id': sd.id,
        'switch': sd.switch,
        'status': sd.status,
        'timestamp': temptimestamp,
        'email_timestamp': temptimestamp + datetime.timedelta(minutes=10),
      })
    
    context = {
          'title': f'Ping Lost report',
          'data': data,
    }

    return render(request,'switch/report.html',context)  

def importData(request):
  if request.method == 'GET':

    filepath = f'{BASE_DIR}\\nosairis_sensor_dashboard\\data\\Data_terminals.csv'

    with open(filepath, "rb") as f:
      in_mem_file = BytesIO(f.read())

    data = pd.read_csv(in_mem_file)

    switch_array = []

    for i in data.index:
      # print(f'{data["SW(Switch Lable)"][i]}, {data["T1(Terminal 1)"][i]}, {data["T2(Terminal 2)"][i]}, {data["T3(Terminal 3)"][i]}, {data["T4(Terminal 4)"][i]}, {data["T5(Terminal 5)"][i]}, {data["TS(Unix Timestamp)"][i]}')
      if(data["SW(Switch Lable)"][i] not in switch_array):
        switch_array.append(data["SW(Switch Lable)"][i])
      
      temp_array = [
        data["T1(Terminal 1)"][i],
        data["T2(Terminal 2)"][i],
        data["T3(Terminal 3)"][i],
        data["T4(Terminal 4)"][i],
        data["T5(Terminal 5)"][i],
      ]

      if(1 in temp_array):
        Switch.objects.create(switch = data["SW(Switch Lable)"][i], status = True, timestamp = data["TS(Unix Timestamp)"][i] )
      else:
        Switch.objects.create(switch = data["SW(Switch Lable)"][i], status = False, timestamp = data["TS(Unix Timestamp)"][i] )

    SwitchArray.objects.create(switcharray = json.dumps(switch_array))

    context = {
      'title': 'Dashboard',
      'response': 'Data has been succesfully imported.',
      'data': switch_array,
    }

    return render(request,'switch/dashboard.html',context)