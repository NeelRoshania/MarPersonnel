from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy 

# Production Meeting Object/Model
class ProdMeeting(models.Model):
	subject = models.TextField(max_length=50, blank=False)
	insertedAt = models.DateTimeField(auto_now_add=True)
	generatedBy = models.ManyToManyField(User)
	modifiedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_ProdMeeting', null=True)
	updated = models.DateTimeField(auto_now=True)

	def getNotes(self):
		return ProdNote.objects.filter(productionMeeting=self.id)

	def getRMShortages(self):
		return RMShortage.objects.filter(rmStatus__in=['Caution', 'Awaiting Delivery', 'To Place Order',]).order_by('rmShortage')

	def getMaintenanceIssues(self):
		return MaintenanceIssue.objects.filter(active__in=['Unresolved',]).order_by('subject')

	def getOrderPriorities(self):
		from sales.models import OrderPriority
		return OrderPriority.objects.filter(productionMeeting=self.id)

	def getProductionPlans(self):
		return ProductionPlan.objects.filter(status__in=['To Load', 'FOG Fail', 'FOG Pass', 'To drop']).order_by('machine')

	def get_absolute_url(self):
		# return reverse('paint-add', kwargs={'pk': self.pk})
		return reverse('home:index')

	# def __str__(self):
	# 	return self.subject

#Production Note Class
class ProdNote(models.Model):
	prodNote = models.TextField(max_length=150, blank=False)
	productionMeeting = models.ManyToManyField(ProdMeeting, blank=False)
	generatedBy = models.ManyToManyField(User)
	insertedAt = models.DateTimeField(auto_now_add=True)
	modifiedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_ProdNote', null=True)
	updated = models.DateTimeField(auto_now=True)

	def get_absolute_url(self):
		# return reverse('paint-add', kwargs={'pk': self.pk})
		return reverse('home:index')

	def __str__(self):
		return self.prodNote

#Production Note Class
class ProductionPlan(models.Model):
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
    ('Hand Mixed', 'Hand Mixed'),
    ('Lab Jar Mill', 'Lab Jar Mill'),
    ('Lab Hi Speed', 'Lab Hi Speed'),
	)

	STATUS = (
    ('To Load', 'To Load'),
    ('FOG Fail', 'FOG Fail'),
    ('FOG Pass', 'FOG Pass'),
    ('To drop', 'To drop'),
    ('Dropped', 'Dropped'),
	)

	productionMeeting = models.ManyToManyField(ProdMeeting, blank=True)
	machine = models.CharField(max_length=14, choices=MACHINE_TYPE, blank=False)
	batchNumber = models.CharField(max_length=20, blank=False)
	productDescription = models.CharField(max_length=50, blank=False)
	status = models.CharField(max_length=8, choices=STATUS, blank=False)
	generatedBy = models.ManyToManyField(User)
	insertedAt = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	modifiedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_ProductionPlan', null=True)

	def get_absolute_url(self):
		# return reverse('paint-add', kwargs={'pk': self.pk})
		return reverse('home:index')

	def __str__(self):
		return '{}, {}'.format(self.machine, self.productDescription)

class RMReference(models.Model):
	
	generatedBy = models.ManyToManyField(User)
	insertedAt = models.DateTimeField(auto_now_add=True)
	rmCode = models.CharField(max_length=10, blank=False)
	rmDescription = models.CharField(max_length=80, blank=False)
	rmWarningLevel = models.IntegerField(blank=True, null=True)
	modifiedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_RMReference', null=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '{}: {}'.format(self.rmCode, self.rmDescription)

	class Meta:
		ordering = ['rmCode']

#Production RMShortage/Reference Class
class RMShortage(models.Model):


	SHORTAGE_STATUS = (
	('Caution', 'Caution'),
    ('Awaiting Delivery', 'Awaiting Delivery'),
    ('To Place Order', 'To Place Order'),
    ('Resolved', 'Resolved'),
	)

	LEVEL_UNIT = (
	('Kg', 'Kg'),
    ('Ltr', 'Ltr'),
	)

	rmShortage = models.ManyToManyField(RMReference, blank=False)
	rmLevel = models.IntegerField(blank=True, null=True)
	rmLevelUnit = models.CharField(max_length=3, choices=LEVEL_UNIT, default='Kg')
	nextDelivery = models.DateField(blank=True, null=True)
	nextDeliveryRef = models.CharField(max_length=20, blank=True, null=True)
	productionMeeting = models.ManyToManyField(ProdMeeting, blank=False)
	rmStatus = models.CharField(max_length=17, choices=SHORTAGE_STATUS, blank=False)
	generatedBy = models.ManyToManyField(User)
	insertedAt = models.DateTimeField(auto_now_add=True)
	resolvedAt = models.DateTimeField(auto_now=True)
	modifiedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_RMShortage', null=True)

	def get_absolute_url(self):
		# return reverse('paint-add', kwargs={'pk': self.pk})
		return reverse('home:index')

	def __str__(self):
		return 'Raw material shortage: {} at {}'.format(self.rmShortage.all()[0], self.rmLevel)

#Maintenance
class MaintenanceIssue(models.Model):
	MAINTENANCE_TYPE = (
    ('Other', 'Other'),
    ('Lab Scale', 'Lab Scale'),
    ('Ball Mill', 'Ball Mill'),
    ('High Speed', 'High Speed'),
    ('Fork Lift', 'Fork Lift'),
    ('Slow Speed', 'Slow Speed'),
	)

	ACTIVE_STATUS = (
    ('Unresolved', 'Unresolved'),
    ('Completed', 'Completed'),
	)

	maintenanceType = models.CharField(max_length=20, choices=MAINTENANCE_TYPE, blank=False)
	subject = models.CharField(max_length=50, blank=False)
	note = models.TextField(max_length=150, blank=False)
	active = models.CharField(max_length=12, choices=ACTIVE_STATUS, blank=False)
	productionMeeting = models.ManyToManyField(ProdMeeting, blank=False, null=True)
	generatedBy = models.ManyToManyField(User)
	insertedAt = models.DateTimeField(auto_now_add=True)
	completedAt = models.DateTimeField(auto_now=True)
	modifiedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_MaintenanceIssue', null=True)
	def get_absolute_url(self):
		# return reverse('paint-add', kwargs={'pk': self.pk})
		return reverse('home:index')

	def __str__(self):
		return '{}: {}'.format(self.maintenanceType, self.subject)
