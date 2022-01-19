from django.urls import path

from .views import register,logout,welcome,Update
from rest_framework.authtoken.views import obtain_auth_token



urlpatterns = [
    path('register/',register.as_view(),name='register'),
    path('login/',obtain_auth_token,name='login'),
    path('logout/',logout.as_view(),name='logout'),
    path('welcome/',welcome.as_view(),name='welcome'),

    path('put/<user_id>',Update.as_view(),name='put'),

]