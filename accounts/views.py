from .forms import PaymentForm, PaymentMethodForm
from .models import Payment, PaymentMethod
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_http_methods
import json
import random
import hashlib

from .models import (
    Apartment, Unit, Tenant, Visitor, Payment, Bill, PaymentMethod, OtherCharges, PasswordResetCode
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
            return redirect("home")
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
    charges = OtherCharges.objects.select_related("bill").order_by("-id")[:5]

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
    return render(request, "accounts/home.html", context)


@login_required
def home(request):
    return render(request, "accounts/home.html")


# ---------------------- TENANTS / UNITS / RENT PAGES ----------------------

@login_required
def tenants(request):
    tenants = Tenant.objects.all()
    form = TenantForm()
    return render(request, "accounts/tenants.html", {"tenants": tenants, "form": form})


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
@csrf_exempt
def apartment_create(request):
    if request.method == "POST":
        # if sync sends JSON (from IndexedDB)
        if request.headers.get("Content-Type") == "application/json":
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)
        else:
            data = request.POST

        Apartment.objects.create(
            name=data.get("name"),
            address=data.get("address"),
            number_of_units=data.get("number_of_units"),
            number_of_tenants=data.get("number_of_tenants"),
            status=data.get("status", "active")
        )

        # If it’s a JSON sync, respond with JSON success
        if request.headers.get("Content-Type") == "application/json":
            return JsonResponse({"success": True})

        # Otherwise normal redirect
        return redirect("apartment_list")

    return render(request, "accounts/apartment_form.html", {"form": ApartmentForm()})


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
    form = UnitForm()
    return render(request, "accounts/unit_list.html", {"units": units, "form": form})


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
        # Return simple success for AJAX
        return JsonResponse({"success": True})
    # For normal GET (render inside tenants.html overlay)
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
    form = BillForm()
    return render(request, "accounts/bill_list.html", {"bills": bills, "form": form})


@login_required
def bill_create(request):
    if request.method == "POST":
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.room_price = bill.unit.price  # ✅ Keep your logic
            bill.save()
            return redirect("bill_list")
    else:
        form = BillForm()

    return render(request, "accounts/bill_form.html", {"form": form})


# ------------------------------------------------------------------
# PAYMENT VIEWS
# ------------------------------------------------------------------

@login_required
def payment_list(request):
    payments = Payment.objects.all().order_by('-date_of_payment')
    form = PaymentForm()
    return render(request, "accounts/payment_list.html", {"payments": payments, "form": form})


@login_required
def payment_create(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)

            # optional: handle bill relationship safely
            bill_id = request.POST.get('bill')
            if bill_id:
                try:
                    bill = Bill.objects.get(pk=bill_id)
                    payment.bill = bill
                except Bill.DoesNotExist:
                    pass

            payment.save()
            return redirect('payment_list')
    else:
        form = PaymentForm()

    bills = Bill.objects.all()
    return render(request, 'accounts/payment_form.html', {'form': form, 'bills': bills})


@login_required
def payment_update(request, pk):
    payment = get_object_or_404(Payment, pk=pk)

    # ✅ Ensure dropdown always has options
    if not PaymentMethod.objects.exists():
        PaymentMethod.objects.bulk_create([
            PaymentMethod(name="Cash"),
            PaymentMethod(name="Gcash"),
            PaymentMethod(name="Bank Transfer"),
        ])

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
    payment.delete()
    return redirect("payment_list")


# ------------------------------------------------------------------
# PAYMENT METHOD VIEWS
# ------------------------------------------------------------------

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


# ---------------------- OTHER CHARGES ----------------------

@login_required
def other_charges_list(request):
    charges = OtherCharges.objects.select_related("bill").all()
    form = OtherChargesForm()
    return render(request, "accounts/other_charges_list.html", {"charges": charges, "form": form})


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

# ---------------------- OFFLINE SYNC ENDPOINT ----------------------


@csrf_exempt
def sync_apartment(request):
    """
    Called automatically when user goes online.
    Accepts JSON from IndexedDB and saves it to the PostgreSQL DB (Supabase).
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            # create Apartment record
            Apartment.objects.create(
                name=data.get("name", "Unnamed Apartment"),
                address=data.get("address", ""),
                number_of_units=data.get("number_of_units") or 0,
                number_of_tenants=data.get("number_of_tenants") or 0,
                status=data.get("status", "active")
            )

            return JsonResponse({"success": True, "message": "Synced successfully!"}, status=201)

        except Exception as e:
            print("❌ Sync error:", e)
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


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

# ---------------------- PASSWORD RESET ----------------------

def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_rate_limit(ip_address):
    """Check if IP has exceeded rate limit for password reset"""
    from django.conf import settings
    window_start = timezone.now() - timedelta(seconds=settings.PASSWORD_RESET_RATE_WINDOW)
    
    recent_requests = PasswordResetCode.objects.filter(
        ip_address=ip_address,
        created_at__gte=window_start
    ).count()
    
    return recent_requests < settings.PASSWORD_RESET_RATE_LIMIT


@csrf_exempt
@require_http_methods(["POST"])
def request_password_reset(request):
    """
    Endpoint: /auth/request-reset/
    Accepts POST with JSON: {"email": "user@example.com"}
    Returns JSON: {"status": "ok"} or {"status": "error", "message": "..."}
    """
    try:
        # Parse JSON request
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
        
        email = data.get('email', '').strip().lower()
        
        if not email:
            return JsonResponse({"status": "error", "message": "Email is required"}, status=400)
        
        # Validate email format
        if '@' not in email or '.' not in email:
            return JsonResponse({"status": "error", "message": "Invalid email format"}, status=400)
        
        # Get client IP for rate limiting
        ip_address = get_client_ip(request)
        
        # Check rate limit
        if not check_rate_limit(ip_address):
            return JsonResponse({
                "status": "error",
                "message": "Too many reset requests. Please try again later."
            }, status=429)
        
        # Check if user exists (for security, we don't reveal if email exists)
        # Always return success to prevent email enumeration
        user_exists = User.objects.filter(email=email).exists()
        
        # Generate 6-digit code
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        # Set expiry to 15 minutes from now
        expires_at = timezone.now() + timedelta(minutes=15)
        
        # Invalidate any existing codes for this email
        PasswordResetCode.objects.filter(email=email, used=False).update(used=True)
        
        # Create new reset code
        reset_code = PasswordResetCode.objects.create(
            email=email,
            code=code,
            expires_at=expires_at,
            ip_address=ip_address
        )
        
        # Only send email if user exists
        if user_exists:
            # Send email with reset code
            subject = "Password Reset Code - Monterde Apartment"
            message = f"""Hello,

You have requested to reset your password for your Monterde Apartment account.

Your password reset code is: {code}

This code will expire in 15 minutes.

If you didn't request this password reset, please ignore this email.

Best regards,
Monterde Apartment Team"""
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                print(f"[OK] Password reset email sent to {email} with code {code}")
            except Exception as e:
                # Log error for debugging
                error_msg = str(e)
                print(f"[ERROR] Email sending failed for {email}: {error_msg}")
                # Still return success to prevent email enumeration
                return JsonResponse({"status": "ok"})
        
        # Always return success (security: don't reveal if email exists)
        return JsonResponse({"status": "ok"})
        
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    except Exception as e:
        # Log error but return generic message
        print(f"Password reset error: {str(e)}")
        return JsonResponse({"status": "error", "message": "An error occurred. Please try again."}, status=500)


def forgot_password_view(request):
    """Render the forgot password page"""
    return render(request, "accounts/forgot_password.html")
