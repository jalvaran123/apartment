# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('home/', views.home, name='home'),

    # Apartments
    path('apartments/', views.apartment_list, name='apartment_list'),
    path('apartments/create/', views.apartment_create, name='apartment_create'),
    path('apartments/update/<int:pk>/', views.apartment_update, name='apartment_update'),
    path('apartments/delete/<int:pk>/', views.apartment_delete, name='apartment_delete'),

    # Units
    path('units/', views.unit_list, name='unit_list'),
    path('units/create/', views.unit_create, name='unit_create'),
    path('units/update/<int:pk>/', views.unit_update, name='unit_update'),
    path('units/delete/<int:pk>/', views.unit_delete, name='unit_delete'),

    # Tenants (canonical name: 'tenants')
    path('tenants/', views.tenants, name='tenants'),
    # alias kept for backward compatibility (some templates pointed to 'tenant_list')
    path('tenants/list/', views.tenants, name='tenant_list'),

    path('tenants/create/', views.tenant_create, name='tenant_create'),
    path('tenants/update/<int:pk>/', views.tenant_update, name='tenant_update'),
    path('tenants/delete/<int:pk>/', views.tenant_delete, name='tenant_delete'),
    path('tenants/assign/<int:tenant_pk>/<int:unit_pk>/', views.assign_tenant_to_unit, name='assign_tenant_to_unit'),

    # Visitors
    path('visitors/', views.visitor_list, name='visitor_list'),
    path('visitors/create/', views.visitor_create, name='visitor_create'),

    # Bills
    path('bills/', views.bill_list, name='bill_list'),
    path('bills/create/', views.bill_create, name='bill_create'),

    # Payments
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/create/', views.payment_create, name='payment_create'),
    path('payments/<int:pk>/edit/', views.payment_update, name='payment_update'),
    path('payments/<int:pk>/delete/', views.payment_delete, name='payment_delete'),

    path('payment_methods/create/', views.payment_method_create, name='payment_method_create'),

    # Rent + Reminders + simple static rent page
    path('rent/', views.rent, name='rent'),
    path('reminders/', views.rent_reminders, name='rent_reminders'),
]
