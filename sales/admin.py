from django.contrib import admin
from .models import CustomerID, DeliveryPlan

# Register your models here.
admin.site.register(CustomerID)
admin.site.register(DeliveryPlan)