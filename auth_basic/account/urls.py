from django.urls import path
from .views import home,loginview,logoutview,registerview,password_reset_request

urlpatterns=[
    path('',home,name='home'),
    path('v1/',loginview,name='login'),
    path('v2/',logoutview,name='logout'),
    path('v3/',registerview,name='register'),
    path("password_reset", password_reset_request, name="password_reset"),

]