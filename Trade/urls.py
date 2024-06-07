from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fetch-analysis/', views.fetch_analysis, name='fetch_analysis'),

]