from .base import FunctionalTest
# from selenium.webdriver.firefox.webdriver import WebDriver
# from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
# from datetime import datetime, date
# import unittest
import time
# import os


# StaticLiveServerTestCase -> serve static files during test, spin up development server for test, creates and deletes test database without interfering with production database
class TestFailedObjectSubmission(FunctionalTest):

	# User makes a submission and observes on objectList
	def test_1_new_userToDo_submission_failure(self):
		# Web request
		self.selenium.get( ('%s%s' % (self.live_server_url, '/')) )
		self.wait_for_(lambda: self.find_object_by_id("updateItem", "ajax loaded."))

		self.insert_UserToDo(
			"", 
			"In Progress", 
			# "2017-2-2222",
			failure=True,
			)	
		print("def test_new_userToDo_submission_failure -> complete")

	# User makes a submission and observes on objectList
	def test_2_new_userNote_submission_failure(self):

		self.wait_for_(lambda: self.find_object_by_id("errorLog", "Form Error in -> subject"))

		# User submits UserToDO and waits for it to upload on the objectList
		self.wait_for_(lambda: self.insert_UserToDo(
			"Test to Search First UserToDo.", 
			"In Progress", 
			# datetime.strftime(date.today(), '%Y-%m-%d'),
			failure=False,
			))
		self.selenium.find_element_by_id('refreshObjectList').click()
		time.sleep(1)
		self.wait_for_(lambda: self.find_object_by_id("UserToDo_subject", "Test to Search First UserToDo."))

		# User Clicks on UserToDo to toggle UserNote, clicks on add button to toggle addUserNoteForm
		self.selenium.find_element_by_id('UserToDo_subject').click()
		time.sleep(1)
		self.selenium.find_element_by_id('addUserNote_Toggle').click()
		time.sleep(1)

		# User inserts a failed UserNote
		self.insert_UserNote(
			"Test to search UserNote", 
			"----------",
			failure=True,
			)
		time.sleep(1)
		self.wait_for_(lambda: self.find_object_by_id("errorLog", "Form Error in -> noteProgress"))

		print("\ndef test_new_userNote_submission_failure -> complete\n")
