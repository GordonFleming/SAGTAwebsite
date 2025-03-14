from django.urls import path
from . import views

urlpatterns = [
	path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
	path('verify-payment/<str:ref>/<str:membership_type>', views.verify_payment, name='verify_payment'),
]