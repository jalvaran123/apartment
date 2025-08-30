from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('home/', views.home, name="home"),
    path('login/', views.login_view, name="login"),
    path('apartments/', views.apartment_list, name='apartment_list'),
    path('apartments/create/', views.apartment_create, name='apartment_create'),
    path('apartments/update/<int:pk>/', views.apartment_update, name='apartment_update'),
    path('apartments/delete/<int:pk>/', views.apartment_delete, name='apartment_delete'),
    path('units/', views.unit_list, name='unit_list'),
    path('units/create/', views.unit_create, name='unit_create'),
    path('units/update/<int:pk>/', views.unit_update, name='unit_update'),
    path('units/delete/<int:pk>/', views.unit_delete, name='unit_delete'),
    path('tenants/', views.tenant_list, name='tenant_list'),
    path('tenants/create/', views.tenant_create, name='tenant_create'),
    path('tenants/update/<int:pk>/', views.tenant_update, name='tenant_update'),
    path('tenants/delete/<int:pk>/', views.tenant_delete, name='tenant_delete'),
    path('tenants/assign/<int:tenant_pk>/<int:unit_pk>/', views.assign_tenant_to_unit, name='assign_tenant_to_unit'),
    path('visitors/', views.visitor_list, name='visitor_list'),
    path('visitors/create/', views.visitor_create, name='visitor_create'),
    path('bills/', views.bill_list, name='bill_list'),
    path('bills/create/', views.bill_create, name='bill_create'),
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/create/', views.payment_create, name='payment_create'),
    path('payment_methods/create/', views.payment_method_create, name='payment_method_create'),
    path('reminders/', views.rent_reminders, name='rent_reminders'),]