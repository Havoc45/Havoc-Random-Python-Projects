from django.urls import path
from . import views

urlpatterns = [
    path('',views.Home,name = 'home'),
    path('view_switch/<str:switchname>/', views.viewSwitch, name = 'view_switch'),
    path('report', views.reportPingLost, name='report'),
    path('import_data',views.importData,name = 'import_data'),
    
]