from django.contrib import admin
from .models import ProdMeeting, ProdNote, RMShortage, MaintenanceIssue, RMReference, ProductionPlan

# Register your models here.
admin.site.register(ProdMeeting)
admin.site.register(ProdNote)
admin.site.register(RMShortage)
admin.site.register(RMReference)
admin.site.register(MaintenanceIssue)
admin.site.register(ProductionPlan)