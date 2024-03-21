from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Inventory
from .serializer import InventorySerializer
from rest_framework import status

#Create your views here

class InventoryItemListAPIView(APIView): 
    def get(self, request, *args, **kwargs): 
        items = Inventory.objects.all() 
        serializer = InventorySerializer(items, many=True) 
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InventoryItemCategoryListAPIView(APIView): 
    def get(self, request, category, *args, **kwargs): 
        items = Inventory.objects.filter(category=category) 
        serializer = InventorySerializer(items, many=True) 
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class InventoryItemSortAPIView(APIView): 
    def get(self, request, *args, **kwargs): 
        items = Inventory.objects.all().order_by('-price') 
        serializer = InventorySerializer(items, many=True) 
        return Response(serializer.data, status=status.HTTP_200_OK)

class InventoryItemEditAPIView(APIView): 
    def put(self, request, item_id, *args, **kwargs): 
        try: 
            item = Inventory.objects.get(id=item_id)
            serializer = InventorySerializer(instance=item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK) 
        except Inventory.DoesNotExist: 
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, item_id, *args, **kwargs): 
        try: 
            item = Inventory.objects.get(id=item_id) 
            item.delete() 
            return Response(status=status.HTTP_204_NO_CONTENT) 
        except Inventory.DoesNotExist: 
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)