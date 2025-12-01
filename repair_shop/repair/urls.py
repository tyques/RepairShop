from django.urls import path

from . import views

app_name = 'repair'

urlpatterns = [
    path('', views.index, name='index'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('appliance-type/<slug:appliance_type_slug>/',
         views.appliance_type_orders, name='appliance_type_orders'),
    path('workshop/<int:workshop_id>/',
         views.workshop_orders, name='workshop_orders'),
]
