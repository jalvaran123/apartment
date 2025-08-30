from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Apartment, Unit, Tenant, Visitor, Payment, Bill, PaymentMethod
from .forms import ApartmentForm, UnitForm, TenantForm, VisitorForm, PaymentForm, BillForm, PaymentMethodForm
from django.utils import timezone
from datetime import timedelta

def index(request):
    return render(request, "accounts/index.html")

@login_required
def home(request):
    return render(request, "accounts/home.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "accounts/login.html", {"error": "Invalid credentials"})
    return render(request, "accounts/login.html")

# Apartment CRUD
@login_required
def apartment_list(request):
    apartments = Apartment.objects.all()
    return render(request, 'accounts/apartment_list.html', {'apartments': apartments})

@login_required
def apartment_create(request):
    if request.method == 'POST':
        form = ApartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('apartment_list')
    else:
        form = ApartmentForm()
    return render(request, 'accounts/apartment_form.html', {'form': form})

@login_required
def apartment_update(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    if request.method == 'POST':
        form = ApartmentForm(request.POST, instance=apartment)
        if form.is_valid():
            form.save()
            return redirect('apartment_list')
    else:
        form = ApartmentForm(instance=apartment)
    return render(request, 'accounts/apartment_form.html', {'form': form})

@login_required
def apartment_delete(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    apartment.delete()
    return redirect('apartment_list')

# Unit CRUD
@login_required
def unit_list(request):
    units = Unit.objects.all()
    return render(request, 'accounts/unit_list.html', {'units': units})

@login_required
def unit_create(request):
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('unit_list')
    else:
        form = UnitForm()
    return render(request, 'accounts/unit_form.html', {'form': form})

@login_required
def unit_update(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('unit_list')
    else:
        form = UnitForm(instance=unit)
    return render(request, 'accounts/unit_form.html', {'form': form})

@login_required
def unit_delete(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    unit.delete()
    return redirect('unit_list')

# Tenant CRUD & Search & Assign
@login_required
def tenant_list(request):
    query = request.GET.get('q')
    if query:
        tenants = Tenant.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(tenant_id__icontains=query)
        )
    else:
        tenants = Tenant.objects.all()
    return render(request, 'accounts/tenant_list.html', {'tenants': tenants})

@login_required
def tenant_create(request):
    if request.method == 'POST':
        form = TenantForm(request.POST)
        if form.is_valid():
            tenant = form.save()
            return redirect('tenant_list')
    else:
        form = TenantForm()
    return render(request, 'accounts/tenant_form.html', {'form': form})

@login_required
def tenant_update(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    if request.method == 'POST':
        form = TenantForm(request.POST, instance=tenant)
        if form.is_valid():
            form.save()
            return redirect('tenant_list')
    else:
        form = TenantForm(instance=tenant)
    return render(request, 'accounts/tenant_form.html', {'form': form})

@login_required
def tenant_delete(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    tenant.delete()
    return redirect('tenant_list')

@login_required
def assign_tenant_to_unit(request, tenant_pk, unit_pk):
    tenant = get_object_or_404(Tenant, pk=tenant_pk)
    unit = get_object_or_404(Unit, pk=unit_pk)
    if unit.current_tenants < unit.max_tenants and unit.status != 'Under Maintenance':
        tenant.unit = unit
        tenant.save()
    return redirect('tenant_list')

# Visitor Log
@login_required
def visitor_create(request):
    if request.method == 'POST':
        form = VisitorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('visitor_list')
    else:
        form = VisitorForm()
    return render(request, 'accounts/visitor_form.html', {'form': form})

@login_required
def visitor_list(request):
    visitors = Visitor.objects.all()
    return render(request, 'accounts/visitor_list.html', {'visitors': visitors})

# Bill Calculation & Payment
@login_required
def bill_create(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.room_price = bill.unit.price  # Auto-set
            bill.save()  # Triggers calculations
            return redirect('bill_list')
    else:
        form = BillForm()
    return render(request, 'accounts/bill_form.html', {'form': form})

@login_required
def bill_list(request):
    bills = Bill.objects.all()
    return render(request, 'accounts/bill_list.html', {'bills': bills})

@login_required
def payment_create(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            payment.rent_status = 'Paid' if payment.amount >= payment.unit.bills.latest('month').total_rent else 'Not Paid'
            payment.save()
            return redirect('payment_list')
    else:
        form = PaymentForm()
    return render(request, 'accounts/payment_form.html', {'form': form})

@login_required
def payment_list(request):
    payments = Payment.objects.all()
    return render(request, 'accounts/payment_list.html', {'payments': payments})

@login_required
def payment_method_create(request):
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_list')
    else:
        form = PaymentMethodForm()
    return render(request, 'accounts/payment_method_form.html', {'form': form})

# Reminder (View due rents a week prior)
@login_required
def rent_reminders(request):
    today = timezone.now().date()
    due_date = today + timedelta(days=7)
    overdue_bills = Bill.objects.filter(month__lte=due_date, payments__isnull=True)
    return render(request, 'accounts/rent_reminders.html', {'overdue_bills': overdue_bills})