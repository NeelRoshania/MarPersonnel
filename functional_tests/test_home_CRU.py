from .base import FunctionalTest
import time
from selenium.common.exceptions import WebDriverException
from datetime import datetime, date
from django.contrib.auth.models import User
# from selenium.webdriver.firefox.webdriver import WebDriver
# from selenium.webdriver.common.keys import Keys
# import unittest
# import os


# StaticLiveServerTestCase -> serve static files during test, spin up development server for test, creates and deletes test database without interfering with production database
class TestNewObjectSubmission(FunctionalTest):

	# User makes a submission and observes on objectList
	def test_1_new_userToDo_UserNote__NoteDescription_submission(self):
		User.objects.create_user('admin', 'admin@testuser.com', 'adminTest')

		# Webpage startup
		self.selenium.get( ('%s%s' % (self.live_server_url, '/')) )
		self.wait_for_(lambda: self.find_object_by_id("loginHeader", "Welcome to Marindec."))
		self.insert_Login(
			"admin", 
			"adminTest",
			)

		self.wait_for_(lambda: self.find_object_by_id("updateItem", "ajax loaded."))

		self.insert_UserToDo(
			"Test New User To Do", 
			"In Progress", 
			failure=False,
			)	
		
		self.selenium.find_element_by_id('refreshObjectList').click()
		self.wait_for_(lambda: self.find_object_by_id("UserToDo_subject", "Test New User To Do"))

		time.sleep(5)

		self.selenium.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		# User inserts a new usernote
		self.selenium.find_element_by_id('UserToDo_subject').click()
		self.wait_for_(lambda: self.find_object_by_id("addUserNote_Toggle", "Insert a task"))
		self.selenium.find_element_by_id('addUserNote_Toggle').click()

		self.insert_UserNote(
			"Test New User Note", 
			"In Progress", 
			# datetime.strftime(date.today(), '%Y-%m-%d'),
			failure=False,
			)	
		time.sleep(5)
		self.selenium.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		self.selenium.find_element_by_id('refreshObjectList').click()
		time.sleep(5)
		self.selenium.find_element_by_id('UserToDo_subject').click()
		time.sleep(1)	# Allow for animation
		self.wait_for_(lambda: self.find_object_by_id("userNote_subject", "Test New User Note"))

		# User inserts a new note description
		self.selenium.find_element_by_id('userNote_subject').click()
		time.sleep(1)	# Allow for animation
		self.selenium.find_element_by_id('addNoteDescription_Toggle').click()
		self.insert_NoteDescription(
			"Test New Note Description", 
			"In Progress",
			)	
		time.sleep(5)
		self.selenium.find_element_by_id('refreshObjectList').click()
		time.sleep(5)
		self.selenium.find_element_by_id('UserToDo_subject').click()
		time.sleep(1)	# Allow for animation
		self.selenium.find_element_by_id('userNote_subject').click()
		time.sleep(1)	# Allow for animation
		self.wait_for_(lambda: self.find_object_by_id("noteDescription_1", "Test New Note Description"))

		# user clicks on edit objective to being making changes to UserToDO
		self.selenium.find_element_by_id('editUserToDo_Toggle').click()

		# Edit objective.
		self.elementID_wait("editUserToDo_heading")
		
		self.edit_UserToDo(
			"Edited New User To Do", 
			"Completed",
			)	
		self.selenium.find_element_by_id('refreshObjectList').click()
		self.wait_for_(lambda: self.find_object_by_id("UserToDo_subject", "Edited New User To Do"))
		print("TEST: test_new_userToDo_submission -> complete")

		# # User decides to make changes to userNote
		# self.selenium.find_element_by_id('UserToDo_subject').click()
		# time.sleep(1)	# Allow for animation
		# self.wait_for_(lambda: self.find_object_by_id("addUserNote_Toggle", "Insert a task"))
		# self.selenium.find_element_by_id('editUserNote_Toggle').click()
		# self.wait_for_(lambda: self.find_object_by_id("editUserNote_heading", "Edit this secondary objective"))
		# self.wait_for_(lambda: self.find_object_by_id("editUserNote_taskNote", "Test New User Note"))
		# self.selenium.execute_script("window.scrollTo(0, 1200)")
		# time.sleep(1)
		# self.edit_UserNote(
		# 	"Edited New User To Do", 
		# 	"Completed",
		# 	)	

		# # User decides to change a note description
		# self.selenium.find_element_by_id('refreshObjectList').click()
		# time.sleep(1)	# Allow for animation
		# self.selenium.find_element_by_id('UserToDo_subject').click()
		# time.sleep(1)	# Allow for animation
		# self.selenium.find_element_by_id('userNote_subject').click()
		# time.sleep(1)	# Allow for animation
		# self.selenium.find_element_by_id('editNoteDescription_Toggle').click()
		# self.edit_NoteDescription(
		# 	"Test New Note Description", 
		# 	"In Progress",
		# 	)	
		# self.selenium.execute_script("window.scrollTo(0, 1200)")
		# time.sleep(1)

		print("\ndef:test_1_new_userToDo_UserNote__NoteDescription_submission -> complete\n")

		return True