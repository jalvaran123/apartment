from django.db import models

class Apartment(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    number_of_units = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Unit(models.Model):
    STATUS_CHOICES = [
        ('Vacant', 'Vacant'),
        ('Occupied', 'Occupied'),
        ('Under Maintenance', 'Under Maintenance'),
    ]
    unit_id = models.AutoField(primary_key=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='units')
    floor = models.IntegerField()
    number_of_tenants = models.IntegerField(default=0)
    max_tenants = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Vacant')

    def __str__(self):
        return f"Unit {self.unit_id} - Floor {self.floor}"

class Tenant(models.Model):
    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    tenant_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    original_address = models.TextField()
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, related_name='tenants')
    move_in_date = models.DateField()
    move_out_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Visitor(models.Model):
    name = models.CharField(max_length=255)
    date_of_visit = models.DateField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='visitors')

    def __str__(self):
        return f"{self.name} visited {self.unit} on {self.date_of_visit}"

class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Payment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='payments')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='payments')
    date_of_payment = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    remarks = models.TextField(blank=True, null=True)
    rent_status = models.CharField(max_length=20, default='Not Paid')

    def __str__(self):
        return f"Payment {self.amount} by {self.tenant} on {self.date_of_payment}"

class Bill(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='bills')
    month = models.DateField()
    room_price = models.DecimalField(max_digits=10, decimal_places=2)
    water_bill = models.DecimalField(max_digits=10, decimal_places=2, default=150.00)
    previous_meter = models.FloatField(default=0)
    current_meter = models.FloatField(default=0)
    electric_bill = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    visitors_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_rent = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_electric_bill(self):
        return (self.current_meter - self.previous_meter) * 11

    def save(self, *args, **kwargs):
        self.electric_bill = self.calculate_electric_bill()
        self.total_rent = self.room_price + self.water_bill + self.electric_bill + self.visitors_charge
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bill for {self.unit} - {self.month.strftime('%B %Y')}"