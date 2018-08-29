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
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from sales.models import CustomerID
from django.contrib.auth.models import User
import time


# StaticLiveServerTestCase -> serve static files during test, spin up development server for test, creates and deletes test database without interfering with production database
class TestEditDeleteObject(FunctionalTest):

	def test_1_editDelete_CustomerID_DeliveryPlan_All(self):
		User.objects.create_user('admin', 'admin@testuser.com', 'adminTest')
		# Web request
		self.selenium.get( ('%s%s' % (self.live_server_url, '/')) )
		self.wait_for_(lambda: self.find_object_by_id("loginHeader", "Welcome to Marindec."))
		self.insert_Login(
			"admin", 
			"adminTest",
			)
		self.wait_for_(lambda: self.find_object_by_id("updateItem", "ajax loaded."))

		# User toggles addDeliveryRoute to add new Customer ID, and accepts the dialog
		self.selenium.find_element_by_id('addDeliveryRoute').click() 
		time.sleep(1)
		self.insert_CustomerID(
			101,
			"testCustomerName",
			"testProcurementName",
			"testProcurementWorkNum",
			"testProcurementEmail@email.com",
			"testTechnicalName",
			"testTechnicalWorkNum",
			"testTechnicalWorkEmail@email.com",
			"Active",
			"Walk-In"
			)

		time.sleep(8)

		# User inserts a delivery meeting, waits for refresh and types in new customer
		time.sleep(1)
		self.selenium.find_element_by_id('addDeliveryRoute').click()
		time.sleep(1) 
		self.selenium.find_element_by_id('deliveryPlan_heading').click() 
		time.sleep(1)

		self.insert_DeliveryPlan(
			"testCustomerName",
			"2018-06-01",
			"2018-05-20",
			"INV10108",
			"Scheduled",
			"Other",
			"Sam is a fucking twat.",
			)	

		time.sleep(1)
		self.wait_for_(lambda: self.find_object_by_id("deliveryPlan_subject", "testCustomerName"))

		# User decides to change details of the CustomerID
		self.selenium.find_element_by_id('addDeliveryRoute').click()
		time.sleep(1)
		self.selenium.find_element_by_id('editCustomerID_heading').click()

		self.edit_CustomerID(
			"testCustomerName",
			101,
			"editCustomerName",
			"editProcurementName",
			"0119084814",
			"editProcurementEmail@email.com",
			"editTechnicalName",
			"0119084813",
			"editTechnicalWorkEmail@email.com",
			"Dormant",
			"Walk-In"
			)	

		self.wait_for_(lambda: self.find_object_by_id("deliveryPlan_subject", "editCustomerName"))

		# User decides to delete Customer ID, user checks to see that delivery plan is deleted as well through refresh prompt
		self.selenium.find_element_by_id('addDeliveryRoute').click()
		time.sleep(1)
		
		self.selenium.find_element_by_id('editCustomerID_heading').click()
		customerSearch_input = self.selenium.find_element_by_id('searchCustomerIDInput')
		customerSearch_input.clear()
		customerSearch_input.send_keys("editCustomerName")
		self.selenium.find_element_by_id("searchCustomerID_Submit").submit()
		time.sleep(1) 
		self.wait_for_(lambda: self.find_object_by_id("customerIDSearchResult_subject", "editCustomerName"))
		time.sleep(5)
		self.selenium.find_element_by_id('deleteCustomerID_Toggle').click()
		time.sleep(1) 
		self.selenium.execute_script("window.scrollBy(0, +200);")
		self.selenium.find_element_by_xpath('//span[@ajaxStatus="deleteCustomerIDForm"]').click()
		time.sleep(3)

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		time.sleep(10)

		print("def:test_1_editDelete_CustomerID_DeliveryPlan_All -> complete")

		return False

