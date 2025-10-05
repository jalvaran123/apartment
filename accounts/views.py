from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import logout

from .models import (
    Apartment, Unit, Tenant, Visitor, Payment, Bill, PaymentMethod, OtherCharges
)
from .forms import (
    ApartmentForm, UnitForm, TenantForm,
    VisitorForm, PaymentForm, BillForm, PaymentMethodForm, OtherChargesForm
)

# ---------------------- AUTH ----------------------


def index(request):
    return render(request, "accounts/index.html")


def logout_view(request):
    logout(request)
    return redirect('login')


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "accounts/login.html", {
                "form": form,
                "error": "Invalid credentials"
            })
    return render(request, "accounts/login.html", {"form": form})


# ---------------------- DASHBOARD ----------------------

@login_required
def dashboard(request):
    tenants = Tenant.objects.select_related("unit__apartment").all()
    units = Unit.objects.select_related("apartment").all()
    payments = Payment.objects.select_related("unit").order_by("-id")[:5]
    bills = Bill.objects.select_related("unit").order_by("-month")[:5]
    charges = OtherCharges.objects.select_related("rent").order_by("-id")[:5]

    stats = {
        "tenant_count": tenants.count(),
        "unit_count": units.count(),
        "payment_count": Payment.objects.count(),
        "bill_count": Bill.objects.count(),
        "charge_count": OtherCharges.objects.count(),
    }

    context = {
        "tenants": tenants,
        "units": units,
        "payments": payments,
        "bills": bills,
        "charges": charges,
        "stats": stats,
    }
    return render(request, "accounts/dashboard.html", context)


@login_required
def home(request):
    return render(request, "accounts/home.html")


# ---------------------- TENANTS / UNITS / RENT PAGES ----------------------

@login_required
def tenants(request):
    tenants_qs = Tenant.objects.select_related("unit__apartment").all()
    return render(request, "accounts/tenants.html", {"tenants": tenants_qs})


@login_required
def units(request):
    units = Unit.objects.select_related("apartment").all()
    return render(request, "accounts/units.html", {"units": units})


@login_required
def rent(request):
    payments = Payment.objects.select_related("unit").all()
    return render(request, "accounts/rent.html", {"payments": payments})


# ---------------------- APARTMENTS CRUD ----------------------

@login_required
def apartment_list(request):
    apartments = Apartment.objects.all()
    return render(request, "accounts/apartment_list.html", {"apartments": apartments})


@login_required
def apartment_create(request):
    form = ApartmentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("apartment_list")
    return render(request, "accounts/apartment_form.html", {"form": form})


@login_required
def apartment_update(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    form = ApartmentForm(request.POST or None, instance=apartment)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("apartment_list")
    return render(request, "accounts/apartment_form.html", {"form": form})


@login_required
def apartment_delete(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    apartment.delete()
    return redirect("apartment_list")


# ---------------------- UNITS CRUD ----------------------

@login_required
def unit_list(request):
    units = Unit.objects.all()
    return render(request, "accounts/unit_list.html", {"units": units})


@login_required
def unit_create(request):
    form = UnitForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("unit_list")
    return render(request, "accounts/unit_form.html", {"form": form})


@login_required
def unit_update(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    form = UnitForm(request.POST or None, instance=unit)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("unit_list")
    return render(request, "accounts/unit_form.html", {"form": form})


@login_required
def unit_delete(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    unit.delete()
    return redirect("unit_list")


# ---------------------- TENANTS CRUD ----------------------

@login_required
def tenant_create(request):
    form = TenantForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("tenants")
    return render(request, "accounts/tenant_form.html", {"form": form})


@login_required
def tenant_update(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    form = TenantForm(request.POST or None, instance=tenant)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("tenants")
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


# ---------------------- VISITORS ----------------------

@login_required
def visitor_list(request):
    visitors = Visitor.objects.all()
    return render(request, "accounts/visitor_list.html", {"visitors": visitors})


@login_required
def visitor_create(request):
    form = VisitorForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("visitor_list")
    return render(request, "accounts/visitor_form.html", {"form": form})


# ---------------------- BILLS & PAYMENTS ----------------------

@login_required
def bill_list(request):
    bills = Bill.objects.select_related("unit").all()
    return render(request, "accounts/bill_list.html", {"bills": bills})


@login_required
def bill_create(request):
    form = BillForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        bill = form.save(commit=False)
        bill.room_price = bill.unit.price
        bill.save()
        return redirect("bill_list")
    return render(request, "accounts/bill_form.html", {"form": form})


@login_required
def payment_list(request):
    payments = Payment.objects.select_related("unit").all()
    return render(request, "accounts/payment_list.html", {"payments": payments})


@login_required
def payment_create(request):
    form = PaymentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        payment = form.save()
        if payment.unit and payment.unit.bills.exists():
            latest_bill = payment.unit.bills.latest("month")
            payment.rent_status = "Paid" if payment.amount >= latest_bill.total_rent else "Not Paid"
            payment.save()
        return redirect("payment_list")
    return render(request, "accounts/payment_form.html", {"form": form})


@login_required
def payment_update(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    form = PaymentForm(request.POST or None, instance=payment)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("payment_list")
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
    form = PaymentMethodForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("payment_list")
    return render(request, "accounts/payment_method_form.html", {"form": form})


# ---------------------- OTHER CHARGES ----------------------
# ---------------------- OTHER CHARGES ----------------------

@login_required
def other_charges_list(request):
    from .models import OtherCharges
    charges = OtherCharges.objects.select_related("bill").all()
    return render(request, "accounts/other_charges_list.html", {"charges": charges})


@login_required
def other_charges_create(request):
    from .forms import OtherChargesForm
    form = OtherChargesForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("other_charges_list")
    return render(request, "accounts/other_charges_form.html", {"form": form})


@login_required
def other_charges_list(request):
    charges = OtherCharges.objects.select_related("rent").all()
    return render(request, "accounts/other_charges_list.html", {"charges": charges})


@login_required
def other_charges_create(request):
    form = OtherChargesForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("other_charges_list")
    return render(request, "accounts/other_charges_form.html", {"form": form})


@login_required
def other_charges_update(request, pk):
    charge = get_object_or_404(OtherCharges, pk=pk)
    form = OtherChargesForm(request.POST or None, instance=charge)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("other_charges_list")
    return render(request, "accounts/other_charges_form.html", {"form": form})


@login_required
def other_charges_delete(request, pk):
    charge = get_object_or_404(OtherCharges, pk=pk)
    charge.delete()
    return redirect("other_charges_list")


# ---------------------- RENT REMINDERS ----------------------

@login_required
def rent_reminders(request):
    today = timezone.now().date()
    due_date = today + timedelta(days=7)
    paid_unit_ids = list(Payment.objects.values_list(
        "unit_id", flat=True).distinct())
    overdue_bills = Bill.objects.filter(
        month__lte=due_date).exclude(unit_id__in=paid_unit_ids)
    return render(request, "accounts/rent_reminders.html", {"overdue_bills": overdue_bills})
