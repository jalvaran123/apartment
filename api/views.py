from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import Apartment, Unit, Tenant, Bill, OtherCharges, Payment, PaymentMethod
from .serializers import (
    ApartmentSerializer,
    UnitSerializer,
    TenantSerializer,
    BillSerializer,
    OtherChargesSerializer,
    PaymentSerializer,
    PaymentMethodSerializer,
)


@api_view(['GET'])
def get_all_data(request):
    data = {
        "apartments": ApartmentSerializer(Apartment.objects.all(), many=True).data,
        "units": UnitSerializer(Unit.objects.all(), many=True).data,
        "tenants": TenantSerializer(Tenant.objects.all(), many=True).data,
        "bills": BillSerializer(Bill.objects.all(), many=True).data,
        "other_charges": OtherChargesSerializer(OtherCharges.objects.all(), many=True).data,
        "payments": PaymentSerializer(Payment.objects.all(), many=True).data,
        "payment_methods": PaymentMethodSerializer(PaymentMethod.objects.all(), many=True).data,
    }
    return Response(data)


@api_view(['GET'])
def get_apartments(request):
    data = ApartmentSerializer(Apartment.objects.all(), many=True).data
    return Response(data)


@api_view(['GET'])
def get_units(request):
    data = UnitSerializer(Unit.objects.all(), many=True).data
    return Response(data)


@api_view(['GET'])
def get_tenants(request):
    data = TenantSerializer(Tenant.objects.all(), many=True).data
    return Response(data)


@api_view(['GET'])
def get_bills(request):
    data = BillSerializer(Bill.objects.all(), many=True).data
    return Response(data)


@api_view(['GET'])
def get_other_charges(request):
    data = OtherChargesSerializer(OtherCharges.objects.all(), many=True).data
    return Response(data)


@api_view(['GET'])
def get_payments(request):
    data = PaymentSerializer(Payment.objects.all(), many=True).data
    return Response(data)


@api_view(['GET'])
def get_payment_methods(request):
    data = PaymentMethodSerializer(PaymentMethod.objects.all(), many=True).data
    return Response(data)
