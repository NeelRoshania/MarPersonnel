# TO run this test -> python manage.py test unit_tests.tests.test_home_models

# List of assertion methods for py TestCase -> https://docs.python.org/3/library/unittest.html#assert-methods

from django.core.urlresolvers import reverse_lazy, reverse
from datetime import datetime, date
from .base import UnitTest
from sales.models import DeliveryPlan, CustomerID
from sales.forms import DeliveryPlanForm, CustomerIDForm
import time

# ModelTests inherits from base class UnitTest
class ModelsTests(UnitTest):

	# Test to see if request posts to HomeView, checks ajax validation, updates model and increments model
	def postTo_View(self, url, data, objectMatch, ajaxConditionals, expectedStatusCode, args=None):
		objects_count = objectMatch.objects.count()	# Get initial object count
		if args:
			response = self.get_httpResponse(url, post=True, post_data=data, ajaxConditionals=ajaxConditionals, args=args)
		else:
			response = self.get_httpResponse(url, post=True, post_data=data, ajaxConditionals=ajaxConditionals)

		# As an ajax call 302 is not called: AjaxFormMixin: form_valid returns a Jsonresponse only. Also, check to see the db inserts correctly
		self.assertEqual(response.status_code, expectedStatusCode)

		# If there are arguments, assume post request for edit object
		if args:
			self.assertEqual(objectMatch.objects.count(), 1)
		else:
			self.assertEqual(objectMatch.objects.count(), objects_count+1)
		# new_object = objectMatch.objects.first()
		# self.assertEqual(new_object.subject, data['subject'])
		print("TEST: postTo_View -> Pass")

	# Test to see that new CustomerID via POST, displays on the UI
	def test_new_CustomerID(self):
		# Create a new CustomerID
		self.postTo_View("sales:index", { 
				'customerCode': "101",
				'customerName': "newCustomerID",
				'procurementName': "procurementName",
				'procurementWorkNum': "0119084813",
				'procurementWorkEmail': "test@email.com",
				'customerStatus': "Active"
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			}, 
			CustomerID, 
			{'ajaxStatus': "addCustomerIDForm"},
			200)
		print("TEST: test_new_CustomerID -> Pass")

	# Test to see that new CustomerID via POST, displays on the UI
	def test_new_DeliveryPlan(self):

		# Create a new CustomerID
		self.postTo_View("sales:index", { 
				'customerCode': "101",
				'customerName': "newCustomerID",
				'procurementName': "procurementName",
				'procurementWorkNum': "0119084813",
				'procurementWorkEmail': "test@email.com",
				'customerStatus': "Active"
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			}, 
			CustomerID, 
			{'ajaxStatus': "addCustomerIDForm"},
			200)

		# Create a DeliveryPlan
		self.postTo_View("sales:index", { 
				'customerID': 1,
				'dateOfDelivery': datetime.strftime(date.today(), '%Y-%m-%d'),
				'invoiceNumber': "INV52101",
				'active': "Scheduled",
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			}, 
			DeliveryPlan, 
			{'ajaxStatus': "addDeliveryNoteForm"},
			200)

		# Check DeliveryPlan updated in home page
		response = self.get_httpResponse("sales:index", post=False)
		self.assertIn('newCustomerID', response.content.decode())

		print("TEST: test_new_DeliveryPlan -> Pass")

	# Test to see that new CustomerID via POST, displays on the UI
	def test_edit_DeliveryPlan_CustomerID(self):

		# Create a new CustomerID
		self.postTo_View("sales:index", { 
				'customerCode': "101",
				'customerName': "newCustomerID",
				'procurementName': "procurementName",
				'procurementWorkNum': "0119084813",
				'procurementWorkEmail': "test@email.com",
				'customerStatus': "Active"
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			}, 
			CustomerID, 
			{'ajaxStatus': "addCustomerIDForm"},
			200)

		# Create a DeliveryPlan
		self.postTo_View("sales:index", { 
				'customerID': 1,
				'dateOfDelivery': datetime.strftime(date.today(), '%Y-%m-%d'),
				'invoiceNumber': "INV52101",
				'active': "Scheduled",
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			}, 
			DeliveryPlan, 
			{'ajaxStatus': "addDeliveryNoteForm"},
			200)

		# Check DeliveryPlan updated in home page
		response = self.get_httpResponse("sales:index", post=False)
		self.assertIn('newCustomerID', response.content.decode())

		# Edit CustomerID
		edit_object = CustomerID.objects.first()
		self.postTo_View("sales:editCustomerID", { 
				'customerCode': "101",
				'customerName': "newCustomerEditID",
				'procurementName': "procurementName",
				'procurementWorkNum': "0119084813",
				'procurementWorkEmail': "test@email.com",
				'customerStatus': "Active"
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			}, 
			CustomerID,
			{'ajaxStatus': "editCustomerIDForm"},
			200,
			args={edit_object.id})

		# Check DeliveryPlan updated in home page
		response = self.get_httpResponse("sales:index", post=False)
		self.assertIn('newCustomerEditID', response.content.decode())

		# Edit DeliveryPlan
		edit_object = DeliveryPlan.objects.first()
		self.postTo_View("sales:edit_DeliveryPlan", { 
				'customerID': 1,
				'dateOfDelivery': datetime.strftime(date.today(), '%Y-%m-%d'),
				'invoiceNumber': "INV52101",
				'active': "Not Delivered",
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			},
			DeliveryPlan,
			{'ajaxStatus': "editDeliveryPlanForm"},
			200,
			args={edit_object.id})

		self.assertEqual('Not Delivered', DeliveryPlan.objects.first().active)

		# Update a DeliveryPlan, check ajax call 302 is not called and check to see the db deletes correctly
		response = self.get_httpResponse(
			"sales:delivered_deliveryPlan", 
			post=True, 
			args={edit_object.id}, 
			ajaxConditionals={'ajaxStatus': "deliveredDeliveryPlanForm"})

		self.assertEqual(response.status_code, 200)
		self.assertEqual(DeliveryPlan.objects.first().active, "Delivered")

		self.assertIn('Object deleted succesfully.', response.content.decode())

		# Delete customerID - deleteCustomerIDForm
		current_obj = CustomerID.objects.count()
		response = self.get_httpResponse(
			"sales:delivered_deliveryPlan", 
			post=True, 
			args={CustomerID.objects.first().id}, 
			ajaxConditionals={'ajaxStatus': "deleteCustomerIDForm"})

		self.assertEqual(response.status_code, 200)
		self.assertEqual(CustomerID.objects.count(), current_obj-1)
		print("TEST: test_edit_DeliveryPlan_CustomerID -> Pass")

# test to search for customerID