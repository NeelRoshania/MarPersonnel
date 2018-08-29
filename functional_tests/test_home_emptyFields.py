from .base import FunctionalTest
# from selenium.webdriver.firefox.webdriver import WebDriver
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import WebDriverException
# from datetime import datetime, date
# import unittest
import time
# import os


# StaticLiveServerTestCase -> serve static files during test, spin up development server for test, creates and deletes test database without interfering with production database
class TestEmptyObjectFields(FunctionalTest):

	# User enters empty UserToDo fields and fails
	def test_1_empty_UserToDo(self):
		# Web startup
		self.selenium.get( ('%s%s' % (self.live_server_url, '/')) )
		self.wait_for_(lambda: self.find_object_by_id("updateItem", "ajax loaded."))

		# User inserts empty data into UserToDo form fields
		self.insert_UserToDo(
			"", 
			"In Progress", 
			# "",
			failure=True,
			)	

		# Page returns error
		self.wait_for_(lambda: self.find_object_by_id("errorLog", "Form Error in -> subject"))
		print("def test_new_object_submission_failure -> complete")

	# User enters empty UserToDo fields and fails
	def test_2_empty_UserNote(self):
		# Web startup
		self.selenium.get( ('%s%s' % (self.live_server_url, '/')) )
		self.wait_for_(lambda: self.find_object_by_id("updateItem", "ajax loaded."))

		# User submits valid UserToDo
		self.insert_UserToDo(
			"Test to Search First UserToDo.", 
			"In Progress", 
			# datetime.strftime(date.today(), '%Y-%m-%d'),
			failure=False,
			)	
		time.sleep(1)
		self.selenium.find_element_by_id('refreshObjectList').click()
		self.wait_for_(lambda: self.find_object_by_id("UserToDo_subject", "Test to Search First UserToDo."))

		# User toggles UserToDo, insert UserNote and inserts empty field data
		self.selenium.find_element_by_id('UserToDo_subject').click()
		time.sleep(1)
		self.selenium.find_element_by_id('addUserNote_Toggle').click()

		# User inserts UserNote
		self.wait_for_(lambda: self.insert_UserNote(
			"", 
			"", 
			# datetime.strftime(date.today(), '%Y-%m-%d'),
			failure=True,
			))

		# Page returns error
		self.wait_for_(lambda: self.find_object_by_id("errorLog", "Form Error in -> noteProgress"))
		
		print("\ndef test_new_object_submission_failure -> complete\n")