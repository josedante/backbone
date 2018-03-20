from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'actualidad'

urlpatterns = [
    path('help-request/received/', views.helprequest_received),
    path('help-request/', views.helprequest),
    path('crm/', views.crm_landing),
    path('website/', views.website_landing),
    path('', views.homepage),
]