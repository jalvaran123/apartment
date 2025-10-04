# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Apartment, Unit, Tenant, Visitor, Payment, Bill, PaymentMethod
from .forms import ApartmentForm, UnitForm, TenantForm, VisitorForm, PaymentForm, BillForm, PaymentMethodForm
from django.utils import timezone
from datetime import timedelta

def index(request):
    return render(request, "accounts/index.html")

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "accounts/login.html", {"form": form, "error": "Invalid credentials"})
    return render(request, "accounts/login.html", {"form": form})

# Dashboard + Home
@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")

@login_required
def home(request):
    return render(request, "accounts/home.html")

# New pages (Tenants / Units / Rent) — these are the UI pages you asked for
@login_required
def tenants(request):
    # fetch tenants and related unit->apartment to avoid N+1
    tenants_qs = Tenant.objects.select_related("unit__apartment").all()
    return render(request, "accounts/tenants.html", {"tenants": tenants_qs})

@login_required
def units(request):
    return render(request, "accounts/units.html")

@login_required
def rent(request):
    return render(request, "accounts/rent.html")

# Apartments CRUD
@login_required
def apartment_list(request):
    apartments = Apartment.objects.all()
    return render(request, "accounts/apartment_list.html", {"apartments": apartments})

@login_required
def apartment_create(request):
    if request.method == "POST":
        form = ApartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("apartment_list")
    else:
        form = ApartmentForm()
    return render(request, "accounts/apartment_form.html", {"form": form})

@login_required
def apartment_update(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    if request.method == "POST":
        form = ApartmentForm(request.POST, instance=apartment)
        if form.is_valid():
            form.save()
            return redirect("apartment_list")
    else:
        form = ApartmentForm(instance=apartment)
    return render(request, "accounts/apartment_form.html", {"form": form})

@login_required
def apartment_delete(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    apartment.delete()
    return redirect("apartment_list")

# Units CRUD
@login_required
def unit_list(request):
    units = Unit.objects.all()
    return render(request, "accounts/unit_list.html", {"units": units})

@login_required
def unit_create(request):
    if request.method == "POST":
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("unit_list")
    else:
        form = UnitForm()
    return render(request, "accounts/unit_form.html", {"form": form})

@login_required
def unit_update(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    if request.method == "POST":
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect("unit_list")
    else:
        form = UnitForm(instance=unit)
    return render(request, "accounts/unit_form.html", {"form": form})

@login_required
def unit_delete(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    unit.delete()
    return redirect("unit_list")

# Tenants CRUD (redirect to tenants page)
@login_required
def tenant_create(request):
    if request.method == "POST":
        form = TenantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tenants")
    else:
        form = TenantForm()
    return render(request, "accounts/tenant_form.html", {"form": form})

@login_required
def tenant_update(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    if request.method == "POST":
        form = TenantForm(request.POST, instance=tenant)
        if form.is_valid():
            form.save()
            return redirect("tenants")
    else:
        form = TenantForm(instance=tenant)
    return render(request, "accounts/tenant_form.html", {"form": form})

@login_required
def tenant_delete(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    tenant.delete()
    return redirect("tenants")

@login_required
def assign_tenant_to_unit(request, tenant_pk, unit_pk):
    tenant = get_object_or_404(Tenant, pk=tenant_pk)
    unit = get_object_or_404(Unit, pk=unit_pk)
    if getattr(unit, "current_tenants", 0) < unit.max_tenants and unit.status != "Under Maintenance":
        tenant.unit = unit
        tenant.save()
    return redirect("tenants")

# Visitors
@login_required
def visitor_list(request):
    visitors = Visitor.objects.all()
    return render(request, "accounts/visitor_list.html", {"visitors": visitors})

@login_required
def visitor_create(request):
    if request.method == "POST":
        form = VisitorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("visitor_list")
    else:
        form = VisitorForm()
    return render(request, "accounts/visitor_form.html", {"form": form})

# Bills + Payments
@login_required
def bill_list(request):
    bills = Bill.objects.all()
    return render(request, "accounts/bill_list.html", {"bills": bills})

@login_required
def bill_create(request):
    if request.method == "POST":
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.room_price = bill.unit.price
            bill.save()
            return redirect("bill_list")
    else:
        form = BillForm()
    return render(request, "accounts/bill_form.html", {"form": form})

@login_required
def payment_list(request):
    payments = Payment.objects.all()
    return render(request, "accounts/payment_list.html", {"payments": payments})

@login_required
def payment_create(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            # mark status if linked bill exists for same unit (best-effort)
            if payment.unit and payment.unit.bills.exists():
                latest_bill = payment.unit.bills.latest("month")
                payment.rent_status = "Paid" if payment.amount >= latest_bill.total_rent else "Not Paid"
                payment.save()
            return redirect("payment_list")
    else:
        form = PaymentForm()
    return render(request, "accounts/payment_form.html", {"form": form})

@login_required
def payment_update(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == "POST":
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect("payment_list")
    else:
        form = PaymentForm(instance=payment)
    return render(request, "accounts/payment_form.html", {"form": form})

@login_required
def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == "POST":
        payment.delete()
        return redirect("payment_list")
    return render(request, "accounts/payment_confirm_delete.html", {"payment": payment})

@login_required
def payment_method_create(request):
    if request.method == "POST":
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("payment_list")
    else:
        form = PaymentMethodForm()
    return render(request, "accounts/payment_method_form.html", {"form": form})

# Rent Reminders
@login_required
def rent_reminders(request):
    today = timezone.now().date()
    due_date = today + timedelta(days=7)

    # Safe, simple: exclude bills for units that already have payments recorded (by unit_id).
    paid_unit_ids = list(Payment.objects.values_list("unit_id", flat=True).distinct())
    overdue_bills = Bill.objects.filter(month__lte=due_date).exclude(unit_id__in=paid_unit_ids)

    return render(request, "accounts/rent_reminders.html", {"overdue_bills": overdue_bills})
