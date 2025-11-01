from django.urls import path
from . import views

urlpatterns = [
    # Status endpoint for health checks
    path('status/', views.get_status, name='get_status'),
    
    # All data
    path('all/', views.get_all_data, name='get_all_data'),

    # Apartments
    path('apartments/', views.get_apartments, name='get_apartments'),
    path('apartment/', views.get_apartments, name='get_apartment'),

    # Units
    path('units/', views.get_units, name='get_units'),
    path('unit/', views.get_units, name='get_unit'),

    # Tenants
    path('tenants/', views.get_tenants, name='get_tenants'),
    path('tenant/', views.get_tenants, name='get_tenant'),

    # Bills
    path('bills/', views.get_bills, name='get_bills'),
    path('bill/', views.get_bills, name='get_bill'),

    # Other Charges
    path('other_charges/', views.get_other_charges, name='get_other_charges'),
    path('other_charge/', views.get_other_charges, name='get_other_charge'),

    # Payments
    path('payments/', views.get_payments, name='get_payments'),
    path('payment/', views.get_payments, name='get_payment'),

    # Payment Methods
    path('payment_methods/', views.get_payment_methods,
         name='get_payment_methods'),
    path('payment_method/', views.get_payment_methods, name='get_payment_method'),
]
