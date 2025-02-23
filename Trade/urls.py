from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fetch-analysis/', views.fetch_analysis, name='fetch_analysis'),
    path('stock-table/', views.stock_table, name='stock_table'),
    path('temettu_tablosu/', views.temettu_tablosu, name='temet_table'),
    path('update_lot_adedi/', views.update_lot_adedi, name='update_lot_adedi'),
    path('mum_grafik/', views.mum_grafik, name='mum_grafik'),
    path('fetch_data/', views.fetch_data, name='fetch_data'),  # Yeni view fonksiyonu
    path('settings/', views.settings_view, name='settings'),
    path('settings/edit/<int:pk>/', views.edit_setting, name='edit_setting'),


]

