from django.db import models
from django.contrib.auth.models import User
from sales.models import CustomerID
from production.models import RMReference
from django.core.urlresolvers import reverse

# Create your models here.

# RDProjects
class RDProject(models.Model):
	subject = models.CharField(max_length=50, blank=False)
	insertedAt = models.DateTimeField(auto_now_add=True)
	insertedBy = models.ManyToManyField(User)
	customer = models.ForeignKey(CustomerID, on_delete=models.CASCADE, blank=False)
	instructions = models.CharField(max_length=100, blank=False)
	modifiedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_RDProject', null=True)
	dateEdited = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '{} - {}'.format(self.customer, self.subject)

	class Meta:
		ordering = ['customer']

class ProductType(models.Model):
	productCode = models.CharField(max_length=20, blank=False)
	productDescription = models.CharField(max_length=100, blank=False)
	insertedAt = models.DateTimeField(auto_now_add=True)
	insertedBy = models.ManyToManyField(User)
	modifiedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_ProductType', null=True)
	dateEdited = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '{} {}'.format(self.productCode, self.productDescription)

	class Meta:
		ordering = ['productCode']

# PaintInfo Object/Model
class PaintInfo(models.Model):

	PAINTINF_TYPE = (
    ('Production Batch', 'Production Batch'),
    ('Lab Batch', 'Lab Batch'),
    ('Work Away Batch', 'Work Away Batch'),
    ('Color Tint Batch', 'Color Tint Batch'),
    ('Refill Batch', 'Refill Batch'),
    ('Blending Batch', 'Blending Batch'),
    ('As per Sample', 'As per Sample'),
    ('As per Application', 'As per Application'),
	)

	VISC_UNIT = (
    ('KU', 'KU'),
    ('Seconds', 'Seconds'),
	)

	DRY_UNIT = (
    ('Hour', 'Hour'),
    ('Min', 'Min'),
	)

	DFT_UNIT = (
    ('200um', '200um'),
    ('150um', '150um'),
    ('100um', '100um'),
    ('76um', '76um'),
    ('Bit-free', 'Bit-free'),
	)

	COLOR_SPEC = (
    ('Spectrophotometer', 'Spectrophotometer'),
    ('Visual Match', 'Visual Match'),
    ('Not Required', 'Not Required'),
	)

	ACTIVE_STATUS = (
    ('In Progress', 'In Progress'),
    ('Completed', 'Completed'),
	)

	MACHINE_TYPE = (
    ('BM1', 'BM1'),
    ('BM2', 'BM2'),
    ('BM3', 'BM3'),
    ('BM4', 'BM4'),
    ('BM5', 'BM5'),
    ('BM6', 'BM6'),
    ('BM7', 'BM7'),
    ('BM8', 'BM8'),
    ('BM9', 'BM9'),
    ('High Speed 1', 'High Speed 1'),
    ('High Speed 2', 'High Speed 2'),
    ('PVA High Speed', 'PVA High Speed'),
    ('3 POT', '3 POT'),
    ('Jar Mill 1', 'Jar Mill 1'),
    ('Jar Mill 2', 'Jar Mill 2'),
    ('Jar Mill 3', 'Jar Mill 3'),
    ('Slow Speed 1', 'Slow Speed 1'),
    ('Slow Speed 2', 'Slow Speed 2'),
    ('Slow Speed 3', 'Slow Speed 3'),
    ('Slow Speed 4', 'Slow Speed 4'),
    ('Slow Speed 5', 'Slow Speed 5'),
    ('Slow Speed 6', 'Slow Speed 6'),
    ('Blending Tank A', 'Blending Tank A'),
    ('Blanding Tank B', 'Blanding Tank B'),
    ('Blending Tank C', 'Blending Tank C'),
    ('Blending Tank D', 'Blending Tank D'),
    ('Blending Tank E', 'Blending Tank E'),
	)

	# meetingDate = models.DateTimeField(auto_now=False)
	insertedAt = models.DateTimeField(auto_now_add=True)
	paintInfoType = models.CharField(max_length=18, choices=PAINTINF_TYPE, default='Batch', blank=False)
	premixMachine = models.CharField(max_length=15, choices=MACHINE_TYPE, blank=True, null=True)
	finishingMachine = models.CharField(max_length=15, choices=MACHINE_TYPE, blank=True, null=True)
	productType = models.ForeignKey(ProductType, on_delete=models.CASCADE, blank=False)
	rdProject = models.ForeignKey(RDProject, on_delete=models.CASCADE, blank=True, null=True)
	batchPeriod = models.IntegerField(blank=False)
	batchNumber = models.IntegerField(blank=False)
	initialFog = models.FloatField(blank=True, null=True)
	initialPremixViscosity = models.FloatField(max_length=5, blank=True, null=True)
	finalPremixViscosity = models.FloatField(max_length=5, blank=True, null=True)
	initialViscosityUnit = models.CharField(max_length=7, choices=VISC_UNIT, blank=True, null=True)
	finalSg = models.FloatField(max_length=5, blank=True, null=True)
	finalHardDry = models.FloatField(max_length=5, blank=True, null=True)
	finalHardDryUnit = models.CharField(max_length=4, choices=DRY_UNIT, blank=True, null=True)
	finalTouchDry = models.FloatField(max_length=5, blank=True, null=True)
	finalTouchDryUnit = models.CharField(max_length=4, choices=DRY_UNIT, blank=True, null=True)
	finalDft = models.FloatField(max_length=5, blank=True, null=True)
	finalDftUnit = models.CharField(max_length=5, choices=DFT_UNIT, blank=True, null=True)
	finalOpacity = models.FloatField(max_length=5, blank=True, null=True)
	finalFog = models.FloatField(blank=True, null=True)
	finalViscosity = models.FloatField(max_length=5, blank=True, null=True)
	finalViscosityUnit = models.CharField(max_length=7, choices=VISC_UNIT, blank=True, null=True)
	finalGloss = models.FloatField(max_length=5, blank=True, null=True)
	finalColorDe = models.FloatField(max_length=5, blank=True, null=True)
	finalColorDeSpec = models.CharField(max_length=17, choices=COLOR_SPEC, blank=True, null=True)
	dateIssued = models.DateField(blank=True, null=True)
	dateLoaded = models.DateField(blank=True, null=True)
	datePremixPassed = models.DateField(blank=True, null=True)
	dateFinalPassed = models.DateField(auto_now=True, null=True)
	active = models.CharField(max_length=12, choices=ACTIVE_STATUS, default='In Progress', blank=True, null=True)
	batchInsertedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inserted_PaintInfo_Batch', null=True)
	premixInfoModifiedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_PaintInfo_PremixInfo', null=True)
	batchInfoModifiedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_PaintInfo_BatchInfo', null=True)
	passedBy = models.ManyToManyField(User)

	def getFinishingAdjustments(self):
		return FinishingAdjustment.objects.filter(paintInfo=self.id)

	def __str__(self):
		return '{}/{}: {}'.format(self.batchPeriod, self.batchNumber, self.productType)

class FinishingAdjustment(models.Model):

	ADJUST_UNIT = (
    ('Litre', 'Litre'),
    ('Kg', 'Kg'),
	)

	ADJUST_STAGE = (
    ('Premix Stage', 'Premix Stage'),
    ('Stabilization Stage', 'Stabilization Stage'),
    ('Finishing/Viscosity Stage', 'Finishing/Viscosity Stage'),
    ('Other', 'Other'),
	)

	insertedAt = models.DateTimeField(auto_now_add=True)
	rmCode = models.ForeignKey(RMReference, on_delete=models.CASCADE)
	paintInfo = models.ForeignKey(PaintInfo, on_delete=models.CASCADE)
	adjustmentAmount = models.CharField(max_length=10, blank=False)
	adjustmentUnit = models.CharField(max_length=5, choices=ADJUST_UNIT, blank=False)
	adjustmentStage = models.CharField(max_length=25, choices=ADJUST_STAGE, blank=False)
	insertedBy = models.ManyToManyField(User)
	modifiedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_FinishingAdjustment', null=True)
	dateEdited = models.DateTimeField(auto_now=True)

	def __str__(self):
		return 'Adjustment of {} {} for {}'.format(self.adjustmentAmount, self.rmCode, self.paintInfo)