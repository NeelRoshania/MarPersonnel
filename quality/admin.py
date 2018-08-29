from django.contrib import admin
from quality.models import RDProject, ProductType, PaintInfo, FinishingAdjustment

# Register your models here.
admin.site.register(PaintInfo)
admin.site.register(RDProject)
admin.site.register(ProductType)
admin.site.register(FinishingAdjustment)