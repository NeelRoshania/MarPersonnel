# TO run this test -> python manage.py test unit_tests.tests.test_home_models

# List of assertion methods for py TestCase -> https://docs.python.org/3/library/unittest.html#assert-methods

from django.core.urlresolvers import reverse_lazy, reverse
from datetime import datetime, date
from .base import UnitTest
from production.models import ProdMeeting, RMShortage, MaintenanceIssue, ProdNote, ProductionPlan, RMReference
from production.forms import ProductionMeetingForm, ProductionNoteForm, RMShortageForm, MaintenanceIssueForm, ProductionPlanForm
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

	# Test to see that new production via POST, displays on the UI
	def test_post_prodMeeting(self):
		self.postTo_View("production:index", {
				'subject': "New ProdMeeting", 
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			}, 
			ProdMeeting, 
			{'ajaxStatus': "addProductionMeetingForm" ,'newObjectSubmit': True,},
			200)

		# As 200 is called, a manual get request is made to check updates on UI
		response = self.get_httpResponse("production:index", post=False)
		self.assertIn('New ProdMeeting', response.content.decode())
		print("TEST: test_post_prodMeeting -> Pass")


	# Test to see if request ajax posts to HomeView, and deletes object at DeleteObjectView
	def test_deleteProductionMeeting_DeleteModelView(self):
		# post a new object to the HomeView, get the object id in preparation for delete post
		self.postTo_View("production:index", {
				'subject': "New ProdMeeting", 
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			}, 
			ProdMeeting,
			{'ajaxStatus': "addProductionMeetingForm" ,'newObjectSubmit': True,},
			200)

		objects_count = ProdMeeting.objects.count()	# Get initial object count
		objectToDelete = ProdMeeting.objects.get(subject="New ProdMeeting")
		print("{}{}".format("Model length: ", objects_count))
		print("{}{}".format("id: ", objectToDelete.id))

		# Make a delete post, check ajax call 302 is not called and check to see the db deletes correctly
		response = self.get_httpResponse(
			"production:delete_productionMeeting", 
			post=True, 
			args={objectToDelete.id}, 
			ajaxConditionals={'ajaxStatus': "deleteProductionMeetingForm"})

		self.assertEqual(response.status_code, 200)
		self.assertEqual(ProdMeeting.objects.count(), objects_count-1)
		print("TEST: test_deleteProductionMeeting_DeleteModelView -> Pass")

	# Test to see if request ajax posts to HomeView, retrievs ModelForm, edits and saves form at EditObjectView
	def test_createNew_edit_ProductionMeeting(self):
		
		self.postTo_View("production:index", {
				'subject': "New ProdMeeting", 
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			}, 
			ProdMeeting,
			{'ajaxStatus': "addProductionMeetingForm" ,'newObjectSubmit': True,},
			200)
		# As an ajax call 302 is not called: AjaxFormMixin: form_valid returns a Jsonresponse only. Also, check to see the db inserts correctly
		edit_object = ProdMeeting.objects.first()

		response = self.get_httpResponse("production:edit_ProductionMeeting", post=False, args={edit_object.id})
		self.assertEqual(response.status_code, 200)
		print('{}{}'.format("content-type:", response['content-type']))

		# Check that the instance of form returned is that of ModelForm, UserToDoForm, and value containes object_name
		self.assertIsInstance(response.context['subForm'], ProductionMeetingForm)
		self.assertContains(response, "{}{}".format("value=", '\"'+edit_object.subject+'\"'))

		# Edit production meeting
		self.postTo_View("production:edit_ProductionMeeting", {
				'subject': "Edited ProdMeeting",
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			}, 
			ProdMeeting,
			{'ajaxStatus': "editProductionMeetingForm" ,'newObjectSubmit': True,},
			200,
			args={edit_object.id})

		# Ensure change is reflect in BaseView response
		response = self.get_httpResponse("production:edit_ProductionMeeting", post=False, args={edit_object.id})
		self.assertIsInstance(response.context['subForm'], ProductionMeetingForm)
		self.assertContains(response, "{}{}".format("value=", '\"'+"Edited ProdMeeting"+'\"'))

		print("TEST: test_createNew_edit_ProductionMeeting -> Pass")

	# Create new production meeting, post and get response from EditProductionNoteView 
	def test_createNew_Edit_ProductionNote(self):

		# Create new production meeting
		self.postTo_View("production:index", {
				'subject': "New ProdMeeting", 
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			}, 
			ProdMeeting,
			{'ajaxStatus': "addProductionMeetingForm" ,'newObjectSubmit': True,},
			200)
		print('{}{}'.format("Production meeting: ", ProdMeeting.objects.first().subject))

		# Create a new production note -> Expect 200 (302 if response returned and not Jsonresponse)
		self.postTo_View(
			"production:index", {
				'prodNote': "New ProdNote", 
				'prodMeeting': ProdMeeting.objects.first().id,
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			},
			ProdNote,
			{'ajaxStatus': "addProductionNoteForm" , 'newObjectSubmit': True,},
			200)
		productionNote = ProdNote.objects.first()
		response = self.get_httpResponse("production:edit_ProductionNote", post=False, args={productionNote.id})
		self.assertEqual(response.status_code, 200)
		print('{}{}'.format("content-type:", response['content-type']))

		# Check that the instance of form returned is that of ModelForm, UserToDoForm, and value containes object_name
		self.assertIsInstance(response.context['subForm'], ProductionNoteForm)
		self.assertContains(response, productionNote.prodNote)

		# Edit production note
		self.postTo_View(
			"production:edit_ProductionNote", {
				'prodNote': "Edited ProdNote",
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			}, 
			ProdNote,
			{'ajaxStatus': "editProductionNoteForm" ,'newObjectSubmit': True,},
			200,
			args={productionNote.id})

		# Ensure change is reflected on baseview response
		response = self.get_httpResponse("production:edit_ProductionNote", post=False, args={productionNote.id})
		self.assertIsInstance(response.context['subForm'], ProductionNoteForm)
		self.assertContains(response, "Edited ProdNote")

		print("TEST: test_createNew_ProductionNote -> Pass")

	# Create new production meeting, post and get response from EditProductionNoteView 
	def test_createNew_RMShortage(self):

		# Create new production meeting
		self.postTo_View("production:index", {
				'subject': "New ProdMeeting", 
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			}, 
			ProdMeeting,
			{'ajaxStatus': "addProductionMeetingForm" ,'newObjectSubmit': True,},
			200)
		print('{}{}'.format("Production meeting: ", ProdMeeting.objects.first().subject))

		# Create a new rm shortage -> Expect 200
		RMReference.objects.create(rmCode="101", rmDescription="testRMReference", rmWarningLevel=1201).save()
		self.postTo_View(
				"production:index", {
				'ajaxStatus': "addRMSHortageForm", 
				'rmShortage': 1,
				'rmLevel': 200,
				'rmStatus': "Caution",
				'prodMeeting': ProdMeeting.objects.first().id,
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
				},
				RMShortage,
				{'ajaxStatus': "addRMSHortageForm" , 'newObjectSubmit': True,},
				200,)

		response = self.get_httpResponse("production:edit_RMShortage", post=False, args={ProdMeeting.objects.first().id})
		self.assertEqual(response.status_code, 200)

		# Check that the instance of form returned is that of ModelForm, UserToDoForm, and value containes object_name
		self.assertIsInstance(response.context['subForm'], RMShortageForm)
		self.assertContains(response, RMReference.objects.get(id=1).rmDescription)

		# Edit RM shortage
		RMReference.objects.create(rmCode="101", rmDescription="editRMReference", rmWarningLevel=1201).save()
		self.postTo_View(
			"production:edit_RMShortage", {
				'rmShortage': 2,
				'rmLevel': 200,
				'rmStatus': "Caution",
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			}, 
			RMShortage,
			{'ajaxStatus': "editRMShortageForm" ,'newObjectSubmit': True,},
			200,
			args={RMShortage.objects.first().id})

		# Ensure change is reflected on baseview response
		response = self.get_httpResponse("production:edit_RMShortage", post=False, args={RMShortage.objects.first().id})
		self.assertIsInstance(response.context['subForm'], RMShortageForm)
		self.assertContains(response, RMReference.objects.get(id=2).rmDescription)

		print("TEST: test_createNew_RMShortage -> Pass")

	# Create new production meeting, post and get response from EditProductionNoteView 
	def test_createNew_MaintenanceIssue(self):

		# Create new production meeting
		self.postTo_View("production:index", {
				'subject': "New ProdMeeting", 
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			}, 
			ProdMeeting,
			{'ajaxStatus': "addProductionMeetingForm" ,'newObjectSubmit': True,},
			200)
		print('{}{}'.format("Production meeting: ", ProdMeeting.objects.first().subject))

		# Create a new maintenance issue -> Expect 200
		self.postTo_View(
				"production:index", {
				'ajaxStatus': "addMaintenanceIssueForm",
				'maintenanceType': "Other",
				'subject': "Test subject maintenance issue",
				'note': "Test note maintenance issue",
				'active': "Unresolved",
				'prodMeeting': ProdMeeting.objects.first().id,
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
				},
				MaintenanceIssue,
				{'ajaxStatus': "addMaintenanceIssueForm" , 'newObjectSubmit': True,},
				200,)

		# Edit maintenance issue
		self.postTo_View(
			"production:edit_MaintenanceIssue", {
				'maintenanceType': "Other",
				'subject': "Edited subject maintenance issue",
				'note': "Edited note maintenance issue",
				'active': "Unresolved",
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			}, 
			MaintenanceIssue,
			{'ajaxStatus': "editMaintenanceIssueForm" ,'newObjectSubmit': True,},
			200,
			args={MaintenanceIssue.objects.first().id})

		# Ensure change is reflected on baseview response
		response = self.get_httpResponse("production:edit_MaintenanceIssue", post=False, args={MaintenanceIssue.objects.first().id})
		self.assertIsInstance(response.context['subForm'], MaintenanceIssueForm)
		self.assertContains(response, "Edited subject maintenance issue")

		response = self.get_httpResponse("production:edit_MaintenanceIssue", post=False, args={ProdMeeting.objects.first().id})
		self.assertEqual(response.status_code, 200)

		# Check that the instance of form returned is that of ModelForm, UserToDoForm, and value containes object_name
		self.assertIsInstance(response.context['subForm'], MaintenanceIssueForm)
		self.assertContains(response, MaintenanceIssue.objects.get(id=1).subject)

		print("TEST: test_createNew_RMShortage -> Pass")

	# Create new production meeting, post and get response from EditProductionNoteView 
	def test_createNew_ProductionPlan(self):

		# Create new production meeting
		self.postTo_View("production:index", {
				'subject': "New ProdMeeting", 
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			}, 
			ProdMeeting,
			{'ajaxStatus': "addProductionMeetingForm" ,'newObjectSubmit': True,},
			200)
		print('{}{}'.format("Production meeting: ", ProdMeeting.objects.first().subject))

		# Create a new production plan -> Expect 200
		self.postTo_View(
				"production:index", {
				'ajaxStatus': "addProductionPlanForm",
				'machine': "BM1",
				'batchNumber': "219/34519",
				'productDescription': "New production plan",
				'status': "FOG Fail",
				'prodMeeting': ProdMeeting.objects.first().id,
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
				},
				ProductionPlan,
				{'ajaxStatus': "addProductionPlanForm" , 'newObjectSubmit': True,},
				200,)

		response = self.get_httpResponse("production:edit_ProductionPlan", post=False, args={ProdMeeting.objects.first().id})
		self.assertEqual(response.status_code, 200)

		# Check that the instance of form returned is that of ModelForm, UserToDoForm, and value containes object_name
		self.assertIsInstance(response.context['subForm'], ProductionPlanForm)
		self.assertContains(response, ProductionPlan.objects.get(id=1).productDescription)

		# Edit maintenance issue
		self.postTo_View(
			"production:edit_ProductionPlan", {
				'machine': "BM1",
				'batchNumber': "219/34519",
				'productDescription': "Edited production plan",
				'status': "FOG Fail",
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			}, 
			ProductionPlan,
			{'ajaxStatus': "editProductionPlanForm" ,'newObjectSubmit': True,},
			200,
			args={ProductionPlan.objects.first().id})

		# Ensure change is reflected on baseview response
		response = self.get_httpResponse("production:edit_ProductionPlan", post=False, args={ProductionPlan.objects.first().id})
		self.assertIsInstance(response.context['subForm'], ProductionPlanForm)
		self.assertContains(response, "Edited production plan")

		print("TEST: test_createNew_ProductionPlan -> Pass")

	# # Test to see if request ajax posts to HomeView, retrievs ModelForm, edits and saves form at EditObjectView
	# def test_get_SearchUserToDoView(self):

	# 	# Make a post request to submit and object in objectList
	# 	self.postTo_View_UserToDo({
	# 			'subject': "Test to search user", 
	# 			'toDoProgress': "In Progress", 
	# 			# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
	# 		})

	# 	response = self.get_httpResponse("home:index", post=False)
	# 	self.assertEqual(response.status_code, 200)
	# 	self.assertIn('Test to search user', response.content.decode())

	# 	#Make a get request to SearchUserToDoView, make a search
	# 	_ = {
	# 			'searchObjectFieldText': "Test to search user", 
	# 			'radio': "subject",
	# 		}

	# 	# Make a search and check that returned objectList contains search text
	# 	response = self.get_httpResponse(
	# 		"home:search_object", 
	# 		post=False, 
	# 		post_data=_, 
	# 		ajaxConditionals={'ajaxStatus': 'searchObjectForm', 'searchObjectSubmit': True},)
	# 	print('{}{}'.format("response: ", response))
	# 	self.assertEqual(response.status_code, 200)
	# 	self.assertIn(_["searchObjectFieldText"], response.content.decode())
	# 	print(response.content.decode())
	# 	print("TEST: test_get_SearchUserToDo -> Pass")