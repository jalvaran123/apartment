from django.db import models
from decimal import Decimal  # ✅ Needed for Decimal-safe arithmetic


# ---------------------- APARTMENT ----------------------
class Apartment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]

    name = models.CharField(max_length=255)
    address = models.TextField()
    number_of_units = models.IntegerField(default=0)
    number_of_tenants = models.IntegerField(default=0)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.name


# ---------------------- UNIT ----------------------
class Unit(models.Model):
    ROOM_STATUS_CHOICES = [
        ('O', 'Occupied'),
        ('V', 'Vacant'),
        ('UM', 'Under Maintenance'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]

    unit_id = models.AutoField(primary_key=True)
    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, related_name='units')
    floor = models.IntegerField()
    number_of_tenants = models.IntegerField(default=0)
    max_tenants = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    room_status = models.CharField(
        max_length=5, choices=ROOM_STATUS_CHOICES, default='V')
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"Unit {self.unit_id} - {self.apartment.name}"


# ---------------------- TENANT ----------------------
class Tenant(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]

    tenant_id = models.AutoField(primary_key=True)
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name='tenants')
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    date_of_birth = models.DateField()
    original_address = models.TextField()
    move_in_date = models.DateField()
    move_out_date = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# ---------------------- VISITOR ----------------------
class Visitor(models.Model):
    name = models.CharField(max_length=255)
    date_of_visit = models.DateField()
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name='visitors')

    def __str__(self):
        return f"{self.name} visited {self.unit} on {self.date_of_visit}"


# ---------------------- PAYMENT METHOD ----------------------
class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ---------------------- BILL ----------------------
class Bill(models.Model):
    tenant = models.ForeignKey(
        'Tenant', on_delete=models.CASCADE, related_name='bills', null=True, blank=True
    )
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name='bills')
    month = models.DateField()
    room_price = models.DecimalField(max_digits=10, decimal_places=2)
    water_bill = models.DecimalField(
        max_digits=10, decimal_places=2, default=150.00)
    previous_meter = models.FloatField(default=0)
    current_meter = models.FloatField(default=0)
    electric_bill = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    total_rent = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)

    def calculate_electric_bill(self):
        return Decimal(self.current_meter - self.previous_meter) * Decimal(11)

    def save(self, *args, **kwargs):
        # Step 1: calculate electric and base totals
        self.electric_bill = self.calculate_electric_bill()
        base_total = (
            Decimal(self.room_price or 0)
            + Decimal(self.water_bill or 0)
            + Decimal(self.electric_bill or 0)
        )

        # Step 2: Save first (so Bill gets a primary key)
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Step 3: Only recalc after we have a PK
        total_other = Decimal(0)
        if not is_new:  # only if already saved once
            total_other = sum(
                Decimal(oc.total or 0) for oc in self.other_charges.all()
            )

        # Step 4: Update total_rent if needed
        new_total = base_total + total_other
        if self.total_rent != new_total:
            self.total_rent = new_total
            super().save(update_fields=['total_rent'])

    def __str__(self):
        return f"Bill for {self.unit} - {self.month.strftime('%B %Y')}"


# ---------------------- OTHER CHARGES ----------------------
class OtherCharges(models.Model):
    bill = models.ForeignKey(
        Bill, on_delete=models.CASCADE, related_name='other_charges')
    name = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name} (₱{self.total})"


# ---------------------- PAYMENT ----------------------
class Payment(models.Model):
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name='payments')
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name='payments')
    bill = models.ForeignKey(  # ✅ added connection to Bill
        Bill, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    date_of_payment = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.ForeignKey(
        PaymentMethod, on_delete=models.SET_NULL, null=True)
    remarks = models.TextField(blank=True, null=True)
    rent_status = models.CharField(max_length=20, default='Not Paid')

    def __str__(self):
        return f"Payment ₱{self.amount} by {self.tenant} on {self.date_of_payment}"
