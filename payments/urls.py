from django.urls import path

from payments import views


urlpatterns=[
    path('webhook/boku/authorisation/', views.boku_pin_authorisation_callback),
    path('webhook/boku/charge/', views.boku_charge_payment_callback),
    path('webhook/boku/refund/', views.boku_refund_payment_callback),
]