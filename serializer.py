from rest_framework import serializers


#Create your serializers here. 

from inventoryapp.models import Inventory 

class InventorySerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Inventory 
        fields = "__all__"
