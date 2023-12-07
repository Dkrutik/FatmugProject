from datetime import datetime
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
# Create your views here.
  
class VendorCreateAPIView(APIView):
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            contex = {
            'data': serializer.data,
            'messasge': "created vender data successfully",
            'status': True}
            return Response(contex, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class VedorListAPIView(APIView):
    def get(self,request):
        result = Vendor.objects.all()  
        serializers = VendorSerializer(result, many=True)  
        contex = {
            'data': serializers.data,
            'messasge': "Get all vender data successfully",
            'status': True}
        return Response(contex, status=200)  
    

class VendorDetailView(APIView):
    def get(self, request, id):  
        try:
            vendor = Vendor.objects.get(id=id)
            serializer = VendorSerializer(vendor)
            context = {
                "vendor": serializer.data,
                'message': 'Vendor succefully fetch',
                'status': 'success'
            }
            return Response(context, status=200)
        except Vendor.DoesNotExist:
            return Response({'status': 'error', 'message': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            vendor = Vendor.objects.get(id=id)
            serializer = VendorSerializer(vendor, data=request.data)
            if serializer.is_valid():
                serializer.save()
                context = {
                    'data': serializer.data,
                    'message': 'Vendor updated successfully',
                    'status': 'success'
                }
                return Response(context, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Vendor.DoesNotExist:
            return Response({'status': 'error', 'message': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)    
        
    
    def delete(self,request ,id):
        try:
            # Vendor =Vendor.objects.get(id=id)
            result = get_object_or_404(Vendor, id=id)
            result.delete()
            return Response({"status": "success","data":"vendor is deleted "})
        except Vendor.DoesNotExist:
            return Response({'status': 'error', 'message': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)


#####################################  PurchaseOrder ##########################################
class PurchaseOrderCreateAPIView(APIView):
    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            contex = {
            'data': serializer.data,
            'messasge': "created purchasesorder data successfully",
            'status': True}
            return Response(contex, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PurchaseOrderListAPIView(APIView):
    def get(self, request):
        vendor_id = request.GET.get('vendor_id')  

        if vendor_id:
            purchase_orders = PurchaseOrder.objects.filter(vendor_id=vendor_id)
        else:
            purchase_orders = PurchaseOrder.objects.all()

        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class PurchesDetailView(APIView):
    def get(self, request, id):  
        try:
            purches = PurchaseOrder.objects.get(id=id)
            serializer = PurchaseOrderSerializer(purches)
            context = {
                "vendor": serializer.data,
                'message': 'PurchaseOrder succefully fetch',
                'status': 'success'
            }
            return Response(context, status=200)
        except PurchaseOrder.DoesNotExist:
            return Response({'status': 'error', 'message': 'PurchaseOrder not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            vendor = PurchaseOrder.objects.get(id=id)
            serializer = PurchaseOrderSerializer(vendor, data=request.data)
            if serializer.is_valid():
                serializer.save()
                context = {
                    'data': serializer.data,
                    'message': 'PurchaseOrder updated successfully',
                    'status': 'success'
                }
                return Response(context, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PurchaseOrder.DoesNotExist:
            return Response({'status': 'error', 'message': 'PurchaseOrder not found'}, status=status.HTTP_404_NOT_FOUND)    
        
    
    def delete(self,request ,id):
        try:
            result = get_object_or_404(PurchaseOrder, id=id)
            result.delete()
            return Response({"status": "success","data":"PurchaseOrder is deleted "})
        except PurchaseOrder.DoesNotExist:
            return Response({'status': 'error', 'message': 'PurchaseOrder not found'}, status=status.HTTP_404_NOT_FOUND)
        

################### hire
class VendorPerformanceAPIView(APIView):
    def get(self, request, id):
        try:
            vendor = Vendor.objects.get(id=id)
            performances = HistoricalPerformance.objects.filter(vendor=vendor)
            serializer = HistoricalPerformanceSerializer(performances, many=True)
            
            # Calculate aggregated metrics if needed
            on_time_delivery_rate = performances.aggregate(avg_on_time_delivery_rate=models.Avg('on_time_delivery_rate'))
            quality_rating_avg = performances.aggregate(avg_quality_rating_avg=models.Avg('quality_rating_avg'))
            average_response_time = performances.aggregate(avg_average_response_time=models.Avg('average_response_time'))
            fulfillment_rate = performances.aggregate(avg_fulfillment_rate=models.Avg('fulfillment_rate'))
            
            vendor_metrics = {
                'vendor_name': vendor.name,
                'on_time_delivery_rate': on_time_delivery_rate['avg_on_time_delivery_rate'],
                'quality_rating_avg': quality_rating_avg['avg_quality_rating_avg'],
                'average_response_time': average_response_time['avg_average_response_time'],
                'fulfillment_rate': fulfillment_rate['avg_fulfillment_rate']
            }

            return Response({'vendor_metrics': vendor_metrics, 'performances': serializer.data}, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response({'message': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
        

class UpdateAcknowledgmentAPIView(APIView):
    def post(self, request, id):
        try:
            purchase_order = PurchaseOrder.objects.get(id=id)
            serializer = PurchaseOrderSerializer(purchase_order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(acknowledgment_date=datetime.now()) 
                return Response({'message': 'Acknowledgment updated'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PurchaseOrder.DoesNotExist:
            return Response({'message': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)