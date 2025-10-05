# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # -------------------------
    # Core / Auth
    # -------------------------
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('home/', views.home, name='home'),

    # -------------------------
    # Apartments CRUD
    # -------------------------
    path('apartments/', views.apartment_list, name='apartment_list'),
    path('apartments/create/', views.apartment_create, name='apartment_create'),
    path('apartments/update/<int:pk>/',
         views.apartment_update, name='apartment_update'),
    path('apartments/delete/<int:pk>/',
         views.apartment_delete, name='apartment_delete'),

    # -------------------------
    # Units CRUD
    # -------------------------
    path('units/', views.unit_list, name='unit_list'),
    path('units/create/', views.unit_create, name='unit_create'),
    path('units/update/<int:pk>/', views.unit_update, name='unit_update'),
    path('units/delete/<int:pk>/', views.unit_delete, name='unit_delete'),

    # -------------------------
    # Tenants CRUD + Assignment
    # -------------------------
    # Main tenants page (list + modal add)
    path('tenants/', views.tenants, name='tenants'),

    # Create, Update, Delete
    path('tenants/create/', views.tenant_create, name='tenant_create'),
    path('tenants/update/<int:pk>/', views.tenant_update, name='tenant_update'),
    path('tenants/delete/<int:pk>/', views.tenant_delete, name='tenant_delete'),

    # Assign tenant to unit
    path('tenants/assign/<int:tenant_pk>/<int:unit_pk>/',
         views.assign_tenant_to_unit, name='assign_tenant_to_unit'),

    # -------------------------
    # Visitors
    # -------------------------
    path('visitors/', views.visitor_list, name='visitor_list'),
    path('visitors/create/', views.visitor_create, name='visitor_create'),

    # -------------------------
    # Bills
    # -------------------------
    path('bills/', views.bill_list, name='bill_list'),
    path('bills/create/', views.bill_create, name='bill_create'),

    # -------------------------
    # Payments
    # -------------------------
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/create/', views.payment_create, name='payment_create'),
    path('payments/<int:pk>/edit/', views.payment_update, name='payment_update'),
    path('payments/<int:pk>/delete/', views.payment_delete, name='payment_delete'),
    path('payment_methods/create/', views.payment_method_create,
         name='payment_method_create'),

    # -------------------------
    # Rent & Reminders
    # -------------------------
    path('rent/', views.rent, name='rent'),
    path('reminders/', views.rent_reminders, name='rent_reminders'),

    # -------------------------
    # Other Charges
    # -------------------------
    path('other-charges/', views.other_charges_list, name='other_charges_list'),
    path('other-charges/create/', views.other_charges_create,
         name='other_charges_create'),
    path('other-charges/update/<int:pk>/',
         views.other_charges_update, name='other_charges_update'),
    path('other-charges/delete/<int:pk>/',
         views.other_charges_delete, name='other_charges_delete'),
    # Other Charges
    path('other_charges/', views.other_charges_list, name='other_charges_list'),
    path('other_charges/create/', views.other_charges_create,
         name='other_charges_create'),

    path('logout/', views.logout_view, name='logout'),


]
