from django import forms
from .models import Apartment, Unit, Tenant, Visitor, Payment, Bill, PaymentMethod, OtherCharges


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
        fields = [
            'first_name', 'middle_name', 'last_name',
            'contact_number', 'date_of_birth', 'sex',
            'original_address', 'unit', 'move_in_date'
        ]


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = '__all__'


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['tenant', 'unit', 'bill',
                  'date_of_payment', 'amount', 'method', 'remarks']

        widgets = {
            'date_of_payment': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'class': 'form-control'}),
            'method': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Optional notes...'}),
            'tenant': forms.Select(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'bill': forms.Select(attrs={'class': 'form-control'}),
        }


# ------------------------------
# Dynamic, robust BillForm
# ------------------------------
# Build the BillForm only including fields that actually exist on the Bill model.
_bill_model_fields = [
    f.name for f in Bill._meta.get_fields()
    if getattr(f, "concrete", False) and not getattr(f, "auto_created", False)
]

# Desired fields (appearance/order preference)
_desired_bill_fields = [
    'tenant', 'unit',
    'billing_date', 'due_date', 'month',
    'amount', 'room_price',
    'water_bill', 'previous_meter', 'current_meter', 'visitors_charge',
    'status', 'remarks'
]

# Final fields list limited to actually-present fields in the model
_bill_fields = [n for n in _desired_bill_fields if n in _bill_model_fields]


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = _bill_fields

        widgets = {}
        if 'billing_date' in _bill_fields:
            widgets['billing_date'] = forms.DateInput(attrs={'type': 'date'})
        if 'due_date' in _bill_fields:
            widgets['due_date'] = forms.DateInput(attrs={'type': 'date'})
        if 'month' in _bill_fields:
            widgets['month'] = forms.DateInput(attrs={'type': 'date'})
        if 'amount' in _bill_fields:
            widgets['amount'] = forms.NumberInput(
                attrs={'step': '0.01', 'min': '0'})
        if 'room_price' in _bill_fields:
            widgets['room_price'] = forms.NumberInput(
                attrs={'step': '0.01', 'min': '0'})
        if 'water_bill' in _bill_fields:
            widgets['water_bill'] = forms.NumberInput(
                attrs={'step': '0.01', 'min': '0'})
        if 'previous_meter' in _bill_fields:
            widgets['previous_meter'] = forms.NumberInput()
        if 'current_meter' in _bill_fields:
            widgets['current_meter'] = forms.NumberInput()
        if 'visitors_charge' in _bill_fields:
            widgets['visitors_charge'] = forms.NumberInput(
                attrs={'step': '0.01', 'min': '0'})
        if 'status' in _bill_fields:
            widgets['status'] = forms.Select()
        if 'remarks' in _bill_fields:
            widgets['remarks'] = forms.Textarea(attrs={'rows': 3})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Safely set tenant queryset if tenant field exists
        if 'tenant' in self.fields:
            try:
                # attempt to order by sensible tenant name fields if available
                tenant_name_fields = [
                    f.name for f in Tenant._meta.get_fields()]
                order_fields = []
                if 'first_name' in tenant_name_fields:
                    order_fields.append('first_name')
                if 'last_name' in tenant_name_fields:
                    order_fields.append('last_name')
                if order_fields:
                    self.fields['tenant'].queryset = Tenant.objects.all().order_by(
                        *order_fields)
                else:
                    self.fields['tenant'].queryset = Tenant.objects.all()
            except Exception:
                # don't raise — fallback to default queryset
                pass

        # Safely set unit queryset if unit field exists — attempt to order by apartment name if possible
        if 'unit' in self.fields:
            try:
                # find an apartment "name" field that's actually present
                apt_field_names = [
                    f.name for f in Apartment._meta.get_fields()]
                candidate_names = ['name', 'a_name', 'address', 'a_address']
                apt_name_field = next(
                    (c for c in candidate_names if c in apt_field_names), None)

                qs = Unit.objects.select_related('apartment').all()
                if apt_name_field:
                    # use 'apartment__<field>' ordering if valid
                    order_by_arg = 'apartment__' + apt_name_field
                    try:
                        qs = qs.order_by(order_by_arg)
                    except Exception:
                        # if ordering fails, fallback to unsorted queryset
                        qs = Unit.objects.select_related('apartment').all()
                self.fields['unit'].queryset = qs
            except Exception:
                pass

        # Add a small consistent class to widgets for styling without overriding existing classes
        for name, field in self.fields.items():
            try:
                existing = field.widget.attrs.get('class', '')
                if 'form-control' not in existing:
                    field.widget.attrs['class'] = (
                        existing + ' form-control').strip()
            except Exception:
                # ignore widgets that don't support attrs
                pass


class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = '__all__'


class OtherChargesForm(forms.ModelForm):
    class Meta:
        model = OtherCharges
        fields = ['bill', 'name', 'total', 'description']
        widgets = {
            'bill': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Parking Fee'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '₱0.00'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Short description'}),
        }
