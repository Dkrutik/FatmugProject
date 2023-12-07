from rest_framework import serializers 
from .models import *


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    order_date = serializers.DateTimeField(format='%Y-%m-%d')
    issue_date=serializers.DateTimeField(format='%Y-%m-%d')
    delivery_date=serializers.DateTimeField(format='%Y-%m-%d')
    acknowledgment_date=serializers.DateTimeField(format='%Y-%m-%d')
    class Meta:
        model = PurchaseOrder
        fields = ['po_number','vendor','order_date','delivery_date','items','quantity','status','quality_rating','issue_date','acknowledgment_date']

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
     class Meta:
        model = HistoricalPerformance
        fields = '__all__'
