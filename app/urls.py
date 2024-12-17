from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('containers/<int:container_id>/', container),
    path('transportations/<int:transportation_id>/', transportation),
]