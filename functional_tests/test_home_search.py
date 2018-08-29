from .base import FunctionalTest
# from selenium.webdriver.firefox.webdriver import WebDriver
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import WebDriverException
# from datetime import datetime, date
# import unittest
# import time
# import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# StaticLiveServerTestCase -> serve static files during test, spin up development server for test, creates and deletes test database without interfering with production database
class TestSearchObject(FunctionalTest):
	# Generic search for a UserToDo

	def test_1_search_UserToDo_UserNote(self):
		# Web request
		self.selenium.get( ('%s%s' % (self.live_server_url, '/')) )
		self.wait_for_(lambda: self.find_object_by_id("updateItem", "ajax loaded."))

		# User submits two UserToDO and waits for it to upload on the objectList
		self.insert_UserToDo(
			"Test to Search First UserToDo.", 
			"In Progress", 
			# datetime.strftime(date.today(), '%Y-%m-%d'),
			)	
		self.selenium.find_element_by_id('refreshObjectList').click()
		time.sleep(2)
		self.wait_for_(lambda: self.find_object_by_id("UserToDo_subject", "Test to Search First UserToDo."))

		# User clicks on the id=searchObject and id=search_UserToDo. 
		self.selenium.find_element_by_id('searchObject').click()
		self.selenium.find_element_by_id('search_UserToDo').click()

		# User selects the Subject line, searches for 'Marindec' and waits for UserToDo to appear on objectList
		self.selenium.find_element_by_id('inlineRadio_UserToDo_1').click()
		searchField = self.selenium.find_element_by_id('search_UserToDo_Field')
		submit = self.selenium.find_element_by_id('searchUserToDo_submit')
		searchField.send_keys("First")
		submit.submit()

		time.sleep(1)
		print("def:test_1_search_UserToDo -> UserToDo insert complete")

		# User waits to see that UserToDo reflects on objectList
		# # self.wait_for_(lambda: self.find_object_by_id("UserToDo_subject", "Test to Search First UserToDo."))
		# self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#UserToDo_subject")))

		# User waits to see that UserToDo reflects on objectList
		self.wait_for_(lambda: self.find_object_by_id("UserToDo_subject", "Test to Search First UserToDo."))
		# self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#UserToDo_subject")))
		

		# User Clicks on UserToDo to toggle UserNote, clicks on add button to toggle addUserNoteForm
		self.selenium.find_element_by_id('UserToDo_subject').click()
		time.sleep(1)
		self.selenium.find_element_by_id('addUserNote_Toggle').click()

		# User inserts UserNote
		self.insert_UserNote(
			"Test to search UserNote", 
			"In Progress", 
			# datetime.strftime(date.today(), '%Y-%m-%d'),
			failure=False
			)

		self.selenium.find_element_by_id('refreshObjectList').click()
		time.sleep(1)

		# User waits for userToDo to update before clicking to check if it's updated
		self.selenium.find_element_by_id('UserToDo_subject').click()
		time.sleep(1)
		self.find_object_by_id("userNote_subject", "Test to search UserNote")

		# User cicks on note progress, enters search text and waits for objectList to refresh
		self.selenium.find_element_by_id('search_UserNote').click()
		self.selenium.find_element_by_id('inlineRadio_UserNote_2').click()
		searchField = self.selenium.find_element_by_id('search_UserNote_Field')
		submit = self.selenium.find_element_by_id('searchUserNote_submit')
		searchField.send_keys("UserNote")
		submit.submit()
		time.sleep(1)

		self.find_object_by_id("UserToDo_subject", "Test to Search First UserToDo.")

		print("\ndef:test_1_search_UserToDo_UserNote -> complete\n")

