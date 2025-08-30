from django.contrib import admin
from .models import Apartment, Unit, Tenant, Visitor, PaymentMethod, Payment, Bill

admin.site.register(Apartment)
admin.site.register(Unit)
admin.site.register(Tenant)
admin.site.register(Visitor)
admin.site.register(PaymentMethod)
admin.site.register(Payment)
admin.site.register(Bill)