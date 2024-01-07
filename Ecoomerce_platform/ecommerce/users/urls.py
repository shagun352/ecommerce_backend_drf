from django.urls import path
from .views import *
urlpatterns = [
  path('register',RegisterUserAPIView.as_view()),
  path('login', LoginView.as_view(), name ='login'),
  path('logout', LogoutView.as_view(), name='logout'),
]