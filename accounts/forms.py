from django import forms
from .models import Apartment, Unit, Tenant, Visitor, Payment, Bill, PaymentMethod

class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = '__all__'

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['apartment', 'floor', 'max_tenants', 'price', 'status']

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['first_name', 'middle_name', 'last_name', 'contact_number', 'date_of_birth', 'sex', 'original_address', 'unit', 'move_in_date']

class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = '__all__'

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['tenant', 'unit', 'date_of_payment', 'amount', 'method', 'remarks']

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['unit', 'month', 'room_price', 'water_bill', 'previous_meter', 'current_meter', 'visitors_charge']

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = '__all__'