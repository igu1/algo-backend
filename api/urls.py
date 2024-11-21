from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('buy/', views.BuyOrder.as_view(), name='buy'),
]
