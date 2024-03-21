from django.urls import path 
from django.contrib import admin 
from .views import (InventoryItemListAPIView, 
     InventoryItemCategoryListAPIView, 
     InventoryItemSortAPIView, 
     InventoryItemEditAPIView, 
    )
    


urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('inventory/items/', InventoryItemListAPIView.as_view(), name='inventory_items_list'),
    path('inventory/items/query/<str:category>/', InventoryItemCategoryListAPIView.as_view(), name='inventory_items_by_category'), 
    path('items/query/<str:category>/', InventoryItemCategoryListAPIView.as_view(), name='inventory_items_by_category'), 
    path('items/sort/', InventoryItemSortAPIView.as_view(), name='inventory_items_sort'),
    path('inventory/items/<int:item_id>/', InventoryItemEditAPIView.as_view(), name='inventory_items_edit_delete'),
]