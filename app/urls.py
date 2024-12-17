from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('containers/<int:container_id>/', container_details, name="container_details"),
    path('containers/<int:container_id>/add_to_transportation/', add_container_to_draft_transportation, name="add_container_to_draft_transportation"),
    path('transportations/<int:transportation_id>/delete/', delete_transportation, name="delete_transportation"),
    path('transportations/<int:transportation_id>/', transportation)
]
