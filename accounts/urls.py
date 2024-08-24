from django.urls import path

from . import views

urlpatterns = [
    path('', views.ShowHomepage.as_view(), name='homepage'),
    path('login/', views.Login.as_view(), name='login'),
]
