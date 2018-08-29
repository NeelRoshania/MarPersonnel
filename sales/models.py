from django.db import models
from django.contrib.auth.models import User
from production.models import ProdMeeting
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta, timezone

# Create your models here.

#CustomerID
class CustomerID(models.Model):

	TYPE = (
    ('Cash', 'Cash'),
    ('Account', 'Account'),
    ('Walk-In', 'Walk-In'),
	)

	STATUS = (
    ('Active', 'Active'),
    ('Dormant', 'Dormant'),
	)

	insertedAt = models.DateTimeField(auto_now_add=True)
	customerCode = models.CharField(max_length=8, blank=False)
	customerName = models.CharField(max_length=60, blank=False)
	procurementName = models.CharField(max_length=80,blank=True, null=True)
	procurementWorkNum = models.CharField(max_length=12,blank=True, null=True)
	procurementWorkEmail = models.EmailField(blank=True, null=True)
	technicalName = models.CharField(max_length=20, blank=True, null=True)
	technicalWorkNum = models.CharField(max_length=12, blank=True, null=True)
	technicalWorkEmail = models.EmailField(blank=True, null=True)
	customerStatus = models.CharField(max_length=15, choices=STATUS, blank=False)
	customerType = models.CharField(max_length=15, choices=TYPE, default="Cash", blank=False)
	generatedBy = models.ManyToManyField(User)
	modifiedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_customerID', null=True)
	dateEdited = models.DateTimeField(auto_now=True)

	def getCustomerName(self):
		return self.customerName

	def __str__(self):
		return self.customerName

	class Meta:
		ordering = ['customerName']

#SALES - Delivery Schedule
class DeliveryPlan(models.Model):

	DELAY_REASON = (
    ('Truck Breakdown', 'Truck Breakdown'),
    ('Traffic/Congestion', 'Traffic/Congestion'),
    ('Could not complete planned route', 'Could not complete planned route'),
    ('Other', 'Other'),
	)

	ACTIVE_STATUS = (
	('Scheduled', 'Scheduled'),
    ('Potential Delay', 'Potential Delay'),
    ('Not Delivered', 'Not Delivered'),
    ('Delivered', 'Delivered'),
	)

	insertedAt = models.DateTimeField(auto_now_add=True)
	customerID = models.ForeignKey(CustomerID, on_delete=models.CASCADE, blank=False)
	orderDate = models.DateField(blank=False)
	dateOfDelivery = models.DateField(blank=False)
	invoiceNumber = models.CharField(max_length=30, blank=False)
	active = models.CharField(max_length=15, choices=ACTIVE_STATUS, blank=False)
	delayField = models.CharField(max_length=32, choices=DELAY_REASON, blank=True)
	delayReason = models.CharField(max_length=50, blank=True)
	generatedBy = models.ManyToManyField(User)
	modifiedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_DeliveryPlan', null=True)
	dateEdited = models.DateTimeField(auto_now=True)

	def get_absolute_url(self):
		# return reverse('paint-add', kwargs={'pk': self.pk})
		return reverse('sales:deliverySchedules')

	def isDelayed(self):
		if (datetime.now() > self.dateOfDelivery.date):
			return 'Delayed'
		else:
			return 'On Time!'
		return reverse('sales:deliverySchedules')

	def __str__(self):
		return '{}'.format(self.customerID)