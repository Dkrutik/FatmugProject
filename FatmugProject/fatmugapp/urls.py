from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('add_vendors/', VendorCreateAPIView.as_view(), name='create_vendor'),
    path('list_vendors/', VedorListAPIView.as_view(), name='list_vendor'),   
    path('vendors/<int:id>/', VendorDetailView.as_view(), name='Details_vendor'),

    ################################## PurchaseOrder ########################
    path('add_purches/', PurchaseOrderCreateAPIView.as_view(), name='create_purches'),
    path('list_purches/', PurchaseOrderListAPIView.as_view(), name='list_purches'), 
    path('purches/<int:id>/', PurchesDetailView.as_view(), name='Details_purches'),
    
    ######################################## Metrics ####################
    path("vendors/<int:id>/performance/",VendorPerformanceAPIView.as_view(), name='list_hitro'),
    path("vendors/<int:id>/acknowledge/",UpdateAcknowledgmentAPIView.as_view(), name='add_hitro')
   
]