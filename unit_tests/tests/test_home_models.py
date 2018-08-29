# TO run this test -> python manage.py test unit_tests.tests.test_home_models

# List of assertion methods for py TestCase -> https://docs.python.org/3/library/unittest.html#assert-methods

from django.core.urlresolvers import reverse_lazy, reverse
from datetime import datetime, date
from .base import UnitTest
from home.models import UserToDo
from home.forms import UserToDoForm
import time

# ModelTests inherits from base class UnitTest
class ModelsTests(UnitTest):

	# Test to see if request posts to HomeView, checks ajax validation, updates model and increments model
	def postTo_BaseView_UserToDo(self, data):
		objects_count = UserToDo.objects.count()	# Get initial object count
		response = self.get_httpResponse("home:index", post=True, post_data=data, ajaxConditionals={'ajaxStatus': "addUserToDoForm" ,'newObjectSubmit': True,})

		# As an ajax call 302 is not called: AjaxFormMixin: form_valid returns a Jsonresponse only. Also, check to see the db inserts correctly
		self.assertEqual(response.status_code, 200)
		self.assertEqual(UserToDo.objects.count(), objects_count+1)
		new_object = UserToDo.objects.first()
		self.assertEqual(new_object.subject, data['subject'])
		print("TEST: postTo_BaseView_UserToDo -> Pass")

	# Test to see that new object via POST, displays on the UI
	def test_object_in_objectList(self):
		self.postTo_BaseView_UserToDo({
				'subject': "Test New User To Do", 
				'toDoProgress': "In Progress", 
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			})

		# As 200 is called, a manual get request is made to check updates on UI
		response = self.get_httpResponse("home:index", post=False)
		self.assertIn('Test New User To Do', response.content.decode())
		print("TEST: test_object_in_objectList -> Pass")


	# Test to see if request ajax posts to HomeView, and deletes object at DeleteObjectView
	def test_postTo_DeleteUserToDoView(self):
		# post a new object to the HomeView, get the object id in preparation for delete post
		self.postTo_BaseView_UserToDo({
				'subject': "Test New User To Do", 
				'toDoProgress': "In Progress", 
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			})

		objects_count = UserToDo.objects.count()	# Get initial object count
		objectToDelete = UserToDo.objects.get(subject="Test New User To Do")
		print("{}{}".format("Model length: ", objects_count))
		print("{}{}".format("id: ", objectToDelete.id))

		# Make a delete post, check ajax call 302 is not called and check to see the db deletes correctly
		response = self.get_httpResponse(
			"home:delete_UserToDo", 
			post=True, 
			args={objectToDelete.id}, 
			ajaxConditionals={'ajaxStatus': "deleteUserToDo"})

		self.assertEqual(response.status_code, 200)
		self.assertEqual(UserToDo.objects.count(), objects_count-1)
		print("TEST: postTo_DeleteObjectView -> Pass")

	# Test to see if request ajax posts to HomeView, retrievs ModelForm, edits and saves form at EditObjectView
	def test_get_EditUserToDoView(self):
		objects_count = UserToDo.objects.count()	# Get initial object count
		self.postTo_BaseView_UserToDo({
				'subject': "Test New User To Do", 
				'toDoProgress': "In Progress", 
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			})
		# As an ajax call 302 is not called: AjaxFormMixin: form_valid returns a Jsonresponse only. Also, check to see the db inserts correctly
		edit_object = UserToDo.objects.first()

		response = self.get_httpResponse("home:edit_UserToDO", post=False, args={edit_object.id})
		self.assertEqual(response.status_code, 200)
		print('{}{}'.format("content-type:", response['content-type']))

		# Check that the instance of form returned is that of ModelForm, UserToDoForm, and value containes object_name
		self.assertIsInstance(response.context['subForm'], UserToDoForm)
		self.assertContains(response, "{}{}".format("value=", '\"'+edit_object.subject+'\"'))

		print("TEST: test_get_EditView -> Pass")

	# Test to see if request ajax posts to HomeView, retrievs ModelForm, edits and saves form at EditObjectView
	def test_postTo_EditUserToDoView(self):
		objects_count = UserToDo.objects.count()	# Get initial object count
		self.postTo_BaseView_UserToDo({
				'subject': "Test New User To Do", 
				'toDoProgress': "In Progress", 
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			})

		# As an ajax call 302 is not called: AjaxFormMixin: form_valid returns a Jsonresponse only. Also, check to see the db inserts correctly
		edit_object = UserToDo.objects.first()
		response = self.get_httpResponse("home:edit_UserToDO", post=False, args={edit_object.id})
		self.assertEqual(response.status_code, 200)

		# Check that the instance of form returned is that of ModelForm, UserToDoForm, and value containes object_name
		self.assertIsInstance(response.context['subForm'], UserToDoForm)
		self.assertContains(response, "{}{}".format("value=", '\"'+edit_object.subject+'\"'))

		# Create instance of invalid form, post to EditObjectView, expect 400
		print('{}{}'.format("edit_UserToDO.id: ", edit_object.id))
		_ = {
				'name': "Test Post Edited Object", 
				'toDoProgress': "In Progress", 
				# 'date': "2-2-2-2" 
			}
		response = self.get_httpResponse(
			"home:edit_UserToDO", 
			post=True, 
			post_data=_, 
			args={edit_object.id}, 
			ajaxConditionals={'ajaxStatus': "editObjectForm", 'editObjectSubmit': True})
		self.assertEqual(response.status_code, 400)
		# self.assertContains(response.content.decode(), 'Enter a valid date.')
		# return self.fail('Obey the testing goat!')
		print("TEST: test_postTo_EditUserToDoView -> Pass")

	# Test to see if request ajax posts to HomeView, retrievs ModelForm, edits and saves form at EditObjectView
	def test_get_SearchUserToDoView(self):
		objects_count = UserToDo.objects.count()	# Get initial object count

		# Make a post request to submit and object in objectList
		self.postTo_BaseView_UserToDo({
				'subject': "Test to search user", 
				'toDoProgress': "In Progress", 
				# 'date': datetime.strftime(date.today(), '%Y-%m-%d')
			})

		response = self.get_httpResponse("home:index", post=False)
		self.assertEqual(response.status_code, 200)
		self.assertIn('Test to search user', response.content.decode())

		#Make a get request to SearchUserToDoView, make a search
		_ = {
				'searchObjectFieldText': "Test to search user", 
				'radio': "subject",
			}

		# Make a search and check that returned objectList contains search text
		response = self.get_httpResponse(
			"home:search_object", 
			post=False, 
			post_data=_, 
			ajaxConditionals={'ajaxStatus': 'searchObjectForm', 'searchObjectSubmit': True},)
		print('{}{}'.format("response: ", response))
		self.assertEqual(response.status_code, 200)
		self.assertIn(_["searchObjectFieldText"], response.content.decode())
		print(response.content.decode())
		print("TEST: test_get_SearchUserToDo -> Pass")