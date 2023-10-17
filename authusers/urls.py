from django.urls import path
from .views import CustomSuccessView

urlpatterns = [
    path('check/', CustomSuccessView.as_view(), name='check'),
]