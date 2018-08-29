# This is a functional test powered by unittest -> an automated test from the user perspective
# 	- Refer to https://docs.python.org/2/library/unittest.html
# 	- https://selenium-python.readthedocs.io/getting-started.html
#	- Navigation ->https://selenium-python.readthedocs.io/navigating.html
# 	- Test to check that er've preserved the behavior of the application

# 	- This file was renamed to tests.py wihtin folder of functional_tests
# 	- To run this functional test, python manage.py test functional_tests --liveserver=localhost:8000
# 	- NewVisitortest subclasses LiveServerTestCase

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, TimeoutException
from datetime import datetime, date

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import unittest
import time
import os
import traceback

# Stand-alone Functional test for inherticance by other functional tests
class FunctionalTest(StaticLiveServerTestCase):
	MAX_WAIT = 20
	wait = ''
	# fixtures = ['tests.json']

	# Callback run before/after test
	@classmethod
	def setUpClass(cls):
		super(FunctionalTest, cls).setUpClass()
		# Set up a customer firefox profile
		profile =  webdriver.FirefoxProfile()
		profile.set_preference("dom.moduleScripts.enabled", True)
		cls.selenium = WebDriver(profile)
		# cls.selenium.implicitly_wait(7)
		cls.wait = WebDriverWait(cls.selenium, 20)
		staging_server = os.environ.get('STAGING_SERVER')  
		if staging_server:
		    self.live_server_url = 'http://' + staging_server  

	# Callback run before/after test
	@classmethod
	def tearDownClass(cls):
		# She thinks about paint, gets really bored and leaves
		# cls.selenium.quit()
		pass

	# Replaced with lambda function, a throwaway function 
	# 	-> Initial: Wait for the post request to reflect on the home page
	# 	-> Wait for any function passed into this
	def wait_for_(self, fn):
		startTime = time.time()

		# run the loop until function meets specification
		while True:
			try:
				return fn()
			except (AssertionError, WebDriverException) as e:
				# If the browser has exceeded a 10 second response time, raise and exception
				if time.time() - startTime > self.MAX_WAIT:
					raise e				
				time.sleep(0.5)

	def find_object_by_id(self, elementId, targetText):
		# Check to see if has been updated on the list via ajax
		objectNames = self.selenium.find_elements_by_id(elementId)
		print('%s%s%s' % (['{}'.format(objectName.text) for objectName in objectNames], " found in ", elementId) if len(objectNames) > 0 else ('%s%s%s' % ("----waiting for ", elementId, ' to update.')))
		self.assertIn(targetText, ['{}'.format(objectName.text) for objectName in objectNames])	

	
	def alert_wait(self):
		browser = self.selenium
		try:
			WebDriverWait(browser, 10).until(EC.alert_is_present(),
	                               'Timed out waiting for PA creation ' +
	                               'confirmation popup to appear.')
		except:
			raise TimeoutException("Process timed out!")
			traceback.print_exc()
			print("Alert box not present!")

	def elementID_wait(self, elementID):
		browser = self.selenium
		try:
			WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, elementID)))
		except:
			raise TimeoutException("Process timed out!")
			traceback.print_exc()
			print('Element not present -> {}'.format(elementID))

	# close notifications
	def closeNotifications(self):
		for i in (self.selenium.find_elements_by_id('closeNotification')):
			i.click()

# Insert new object into UserToDo
	def insert_Login(self, 
		object_userName, 
		object_password, 
		date=None,
		failure=None):

		# User searches for inputs to name, email and date into input fields and submits information
		username_input = self.selenium.find_element_by_id('id_username')
		password_input = self.selenium.find_element_by_id('id_password')
		# date_input = self.selenium.find_element_by_id('addObject_date')
		submit = self.selenium.find_element_by_id('submit_login')

		username_input.send_keys(object_userName)
		password_input.send_keys(object_password)
		# date_input.send_keys(date)

		submit.submit()

	# Insert new object into UserToDo
	def insert_UserToDo(self, 
		object_subject, 
		object_toDoProgress, 
		date=None,
		failure=None):

		# User clicks on add object button to toggle form
		print("{}{}".format("addObject:", self.selenium.find_element_by_id('addObject')))
		self.selenium.find_element_by_id('addObject').click()

		# User searches for inputs to name, email and date into input fields and submits information
		subject_input = self.selenium.find_element_by_id('userToDoForm_subject')
		toDoProgress_input = self.selenium.find_element_by_id('userToDoForm_toDoProgress')
		# date_input = self.selenium.find_element_by_id('addObject_date')
		submit = self.selenium.find_element_by_id('addUserToDo_Submit')

		subject_input.send_keys(object_subject)
		toDoProgress_input.send_keys(object_toDoProgress)
		# date_input.send_keys(date)

		submit.submit()

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		if (failure == False): 
			# Success notification
			self.wait_for_(lambda: self.find_object_by_id("notification", "You have new objectives!"))

			# Refresh results to view
			self.wait_for_(lambda: self.find_object_by_id("notification", "Refresh page to view changes!"))
			self.closeNotifications()

	# Insert new object into UserToDo
	def edit_UserToDo(self, 
		object_subject, 
		object_toDoProgress, 
		date=None):

		# User searches for inputs to name, email and date into input fields and submits information
		subject_input = self.selenium.find_element_by_id('editUserToDo_subject')
		toDoProgress_input = self.selenium.find_element_by_id('editUserToDo_toDoProgress')
		submit = self.selenium.find_element_by_id('edit_UserToDo_Submit')

		subject_input.clear()
		subject_input.send_keys(object_subject)
		toDoProgress_input.send_keys(object_toDoProgress)
		# date_input.send_keys(date)

		submit.submit()

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# Success notification
		self.wait_for_(lambda: self.find_object_by_id("notification", "Your objective was modified successfully!"))

		# Refresh results to view
		self.wait_for_(lambda: self.find_object_by_id("notification", "Refresh page to view changes!"))
		self.closeNotifications()

		print("def insert_NewObject -> complete")

	# Insert new object into UserNote
	def insert_UserNote(self, 
		object_taskNote, 
		object_noteProgress, 
		date=None,
		failure=None):

		# User identifies, inserts and submits User Note Data
		noteProgress = self.selenium.find_element_by_id('userNoteForm_noteProgress')
		taskNote = self.selenium.find_element_by_id('userNoteForm_taskNote')
		submit = self.selenium.find_element_by_id('addUserNote_Submit')

		noteProgress.send_keys(object_noteProgress)
		taskNote.send_keys(object_taskNote)
		submit.submit()

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# If UserNote is not expecting a failure
		if (failure == False): 
			# Success notification
			self.wait_for_(lambda: self.find_object_by_id("notification", "Your objective has things to do!"))

			# Refresh results to view
			self.wait_for_(lambda: self.find_object_by_id("notification", "Refresh page to view changes!"))
			self.closeNotifications()
		
		print("def insert_UserNote -> complete")

		return True

	# Insert new object into UserNote
	def edit_UserNote(self, 
		object_taskNote, 
		object_noteProgress, 
		date=None):

		time.sleep(1)
		# User identifies, inserts and submits User Note Data
		taskNote_input = self.selenium.find_element_by_id('editUserNote_taskNote')
		noteProgress_input = self.selenium.find_element_by_id('editUserNote_noteProgress')
		submit = self.selenium.find_element_by_id('edit_UserNote_Submit')

		taskNote_input.clear()
		taskNote_input.send_keys(object_taskNote)
		noteProgress_input.send_keys(object_noteProgress)
		submit.submit()

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# Success notification
		self.wait_for_(lambda: self.find_object_by_id("notification", "Your task was modified successfully!"))

		# Refresh results to view
		self.wait_for_(lambda: self.find_object_by_id("notification", "Refresh page to view changes!"))
		self.closeNotifications()

		print("def insert_UserNote -> complete")

		return True

	# Insert new object into UserNote
	def insert_NoteDescription(self, 
		object_noteDescription, 
		object_noteDescriptionProgress, 
		date=None):

		# User identifies, inserts and submits User Note Data
		noteDescription = self.selenium.find_element_by_id('noteDescriptionForm_description')
		noteDescrptionProgress = self.selenium.find_element_by_id('noteDescriptionForm_noteDescriptionProgress')
		submit = self.selenium.find_element_by_id('addNoteDescription_Submit')

		noteDescription.send_keys(object_noteDescription)
		noteDescrptionProgress.send_keys(object_noteDescriptionProgress)
		submit.submit()

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# Success notification
		self.wait_for_(lambda: self.find_object_by_id("notification", "Your task has a new note!"))

		# Refresh results to view
		self.wait_for_(lambda: self.find_object_by_id("notification", "Refresh page to view changes!"))
		self.closeNotifications()

		print("def insert_NoteDescription -> complete")

		return True

	# Insert new object into UserNote
	def edit_NoteDescription(self, 
		object_noteDescription, 
		object_noteDescriptionProgress, 
		date=None):

		# User identifies, inserts and submits User Note Data
		noteDescription = self.selenium.find_element_by_id('editNoteDescriptionForm_description')
		noteDescrptionProgress = self.selenium.find_element_by_id('editNoteDescriptionForm_noteDescriptionProgress')
		submit = self.selenium.find_element_by_id('edit_NoteDescription_Submit')

		noteDescription.clear()
		noteDescription.send_keys(object_noteDescription)
		noteDescrptionProgress.send_keys(object_noteDescriptionProgress)
		submit.submit()

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# Success notification
		self.wait_for_(lambda: self.find_object_by_id("notification", "Your task has a new note!"))

		# Refresh results to view
		self.wait_for_(lambda: self.find_object_by_id("notification", "Refresh page to view changes!"))
		self.closeNotifications()

		print("def insert_NoteDescription -> complete")

		return True

	# Insert new Production Meeting
	def insert_ProductionMeeting(self, object_subject, date=None):
		# User clicks on addProductionForm button to toggle form
		print("{}{}".format("addProduction:", self.selenium.find_element_by_id('addProduction')))
		self.selenium.find_element_by_id('addProduction').click()
		time.sleep(1)
		self.selenium.find_element_by_id('insertProductionMeeting_heading').click()
		
		# User searches for inputs to name, email and date into input fields and submits information
		subject_input = self.selenium.find_element_by_id('ProductionMeetingForm_subject')
		# date_input = self.selenium.find_element_by_id('addObject_date')
		submit = self.selenium.find_element_by_id('add_ProductionMeeting_Submit')

		subject_input.send_keys(object_subject)
		# date_input.send_keys(date)

		submit.submit()

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# Refresh message
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# Refresh production list because refreshObject set to false
		# self.selenium.find_element_by_id('refreshProductionList').click()
		print("def insert_ProductionMeeting -> complete")

	# Edit existing Production Meeting
	def edit_ProductionMeeting(self, object_subject, date=None):

		# User clicks on editProductionMeeting button to toggle form
		self.selenium.find_element_by_id('editProductionMeeting_Toggle').click()
		self.wait_for_(lambda: self.find_object_by_id("editProductionMeeting_header", "Change the subject of this production meeting."))

		# User searches for inputs to name, email and date into input fields and submits information
		subject_input = self.selenium.find_element_by_id('Edit_ProductionMeetingForm_subject')
		# date_input = self.selenium.find_element_by_id('addObject_date')
		submit = self.selenium.find_element_by_id('edit_ProductionMeeting_Submit')
		subject_input.clear()
		subject_input.send_keys(object_subject)
		# date_input.send_keys(date)

		submit.submit()

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# Refresh message
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept() 

		# Refresh production list because refreshObject set to false
		# self.selenium.find_element_by_id('refreshProductionList').click()
		print("def edit_ProductionMeeting -> complete")

	# Insert new production note
	def insert_ProductionNote(self, object_subject, date=None):

		# User clicks on addProductionNote_Toggle button to toggle form
		self.selenium.find_element_by_id('addProductionNote_Toggle').click()

		# User searches for inputs to name, email and date into input fields and submits information
		prodNote_input = self.selenium.find_element_by_id('ProductionNoteForm_prodNote')
		# date_input = self.selenium.find_element_by_id('addObject_date')
		submit = self.selenium.find_element_by_id('addProductionNote_Submit')

		prodNote_input.send_keys(object_subject)
		# date_input.send_keys(date)

		submit.submit()

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# Refresh message
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept() 


		print("def insert_ProductionNote -> complete")

	# edit existing production note
	def edit_ProductionNote(self, object_subject, date=None):

		# User clicks on addProductionNote_Toggle button to toggle form
		self.selenium.find_element_by_id('editProductionNote_Toggle').click()
		self.wait_for_(lambda: self.find_object_by_id("editProductionNote_header", "Change the information of this production note."))

		# User searches for inputs to name, email and date into input fields and submits information
		prodNote_input = self.selenium.find_element_by_id('Edit_ProductionNoteForm_prodNote')
		# date_input = self.selenium.find_element_by_id('addObject_date')
		submit = self.selenium.find_element_by_id('edit_ProductionNote_Submit')

		prodNote_input.clear()
		prodNote_input.send_keys(object_subject)
		# date_input.send_keys(date)

		submit.submit()

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# Refresh message
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept() 

		print("def insert_ProductionNote -> complete")

	# Insert new CustomerID
	def insert_CustomerID(self, 
		object_customerCode, 
		object_customerName, 
		object_procurementName, 
		object_procurementWorkNum,
		object_procurementEmail, 
		object_technicalName,
		object_technicalWorkNum, 
		object_technicalWorkEmail,
		object_customerStatus,
		object_customerType):

		# User clicks on addDeliveryRoute button to toggle form and DeliveryPlan tag
		print("{}{}".format("addProduction:", self.selenium.find_element_by_id('addProduction')))
		self.selenium.find_element_by_id('addDeliveryRouteForm').click() 
		self.selenium.find_element_by_id('addCustomerID').click()

		customerCode_input = self.selenium.find_element_by_id('CustomerIDForm_customerCode')
		customerName_input = self.selenium.find_element_by_id('CustomerIDForm_customerName')
		procurementName_input = self.selenium.find_element_by_id('CustomerIDForm_procurementName')
		procurementWorkNum_input = self.selenium.find_element_by_id('CustomerIDForm_procurementWorkNum')
		procurementWorkEmail_input = self.selenium.find_element_by_id('CustomerIDForm_procurementWorkEmail')
		technicalName_input = self.selenium.find_element_by_id('CustomerIDForm_technicalName')
		technicalWorkNum_input = self.selenium.find_element_by_id('CustomerIDForm_technicalWorkNum')
		technicalWorkEmail_input = self.selenium.find_element_by_id('CustomerIDForm_technicalWorkEmail')
		customerStatus_input = self.selenium.find_element_by_id('CustomerIDForm_customerStatus')
		customerType_input = self.selenium.find_element_by_id('CustomerIDForm_customerType')


		submit = self.selenium.find_element_by_id('addCustomerID_Submit')
		customerCode_input.send_keys(object_customerCode)
		customerName_input.send_keys(object_customerName)
		procurementName_input.send_keys(object_procurementName)
		procurementWorkNum_input.send_keys(object_procurementWorkNum)
		procurementWorkEmail_input.send_keys(object_procurementEmail)
		technicalName_input.send_keys(object_technicalName)
		technicalWorkNum_input.send_keys(object_technicalWorkNum)
		technicalWorkEmail_input.send_keys(object_technicalWorkEmail)
		customerStatus_input.send_keys(object_customerStatus)
		customerType_input.send_keys(object_customerStatus)

		submit.submit()

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# OK to refresh
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()
		print("def insert_DeliveryPlan -> complete")

	# Edit an existing CustomerID
	def edit_CustomerID(self, 
		object_searchCustomerInput,
		object_customerCode, 
		object_customerName, 
		object_procurementName, 
		object_procurementWorkNum,
		object_procurementEmail, 
		object_technicalName,
		object_technicalWorkNum, 
		object_technicalWorkEmail,
		object_customerStatus,
		object_customerType):

		# User inserts search information, submits and waits for result
		customerSearch_input = self.selenium.find_element_by_id('searchCustomerIDInput')
		self.selenium.find_element_by_id("searchCustomerID_Submit").submit()
		customerSearch_input.send_keys(object_searchCustomerInput)
		time.sleep(1)
		self.wait_for_(lambda: self.find_object_by_id("customerIDSearchResult_subject", "testCustomerName"))
		self.closeNotifications()
		self.selenium.find_element_by_id('editCustomerID_Toggle').click()
		time.sleep(1)

		customerCode_input = self.selenium.find_element_by_id('Edit_DeliveryPlanForm_customerCode')
		customerName_input = self.selenium.find_element_by_id('Edit_DeliveryPlanForm_customerName')
		procurementName_input = self.selenium.find_element_by_id('Edit_DeliveryPlanForm_procurementName')
		procurementWorkNum_input = self.selenium.find_element_by_id('Edit_DeliveryPlanForm_procurementWorkNum')
		procurementWorkEmail_input = self.selenium.find_element_by_id('Edit_DeliveryPlanForm_procurementWorkEmail')
		technicalName_input = self.selenium.find_element_by_id('Edit_DeliveryPlanForm_technicalName')
		technicalWorkNum_input = self.selenium.find_element_by_id('Edit_DeliveryPlanForm_technicalWorkNum')
		technicalWorkEmail_input = self.selenium.find_element_by_id('Edit_DeliveryPlanForm_technicalWorkEmail')
		customerStatus_input = self.selenium.find_element_by_id('Edit_DeliveryPlanForm_customerStatus')
		customerType_input = self.selenium.find_element_by_id('Edit_DeliveryPlanForm_customerType')

		submit = self.selenium.find_element_by_id('edit_CustomerID_Submit')

		customerCode_input.clear()
		customerName_input.clear()
		procurementName_input.clear()
		procurementWorkNum_input.clear()
		procurementWorkEmail_input.clear()
		technicalName_input.clear()
		technicalWorkNum_input.clear()
		technicalWorkEmail_input.clear()

		customerCode_input.send_keys(object_customerCode)
		customerName_input.send_keys(object_customerName)
		procurementName_input.send_keys(object_procurementName)
		procurementWorkNum_input.send_keys(object_procurementWorkNum)
		procurementWorkEmail_input.send_keys(object_procurementEmail)
		technicalName_input.send_keys(object_technicalName)
		technicalWorkNum_input.send_keys(object_technicalWorkNum)
		technicalWorkEmail_input.send_keys(object_technicalWorkEmail)
		customerStatus_input.send_keys(object_customerStatus)
		customerType_input.send_keys(object_customerStatus)

		submit.submit()
		
		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# OK ro refresh
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept() 

		print("def edit_CustomerID -> complete")

	# Insert new Production Meeting
	def insert_DeliveryPlan(self, 
		object_customerID, 
		object_deliveryDate, 
		object_orderPlaced,
		object_invoiceNumber, 
		object_active, 
		object_delayField, 
		object_delayReason):
		
		# User selects form information
		customerID_input = self.selenium.find_element_by_id('DeliveryPlanForm_customerID')
		deliveryDate_input = self.selenium.find_element_by_id('DeliveryPlanForm_dateOfDelivery')
		orderPlacedDate_input = self.selenium.find_element_by_id('DeliveryPlanForm_orderDate')
		invoiceNumber_input = self.selenium.find_element_by_id('DeliveryPlanForm_invoiceNumber')
		active_input = self.selenium.find_element_by_id('DeliveryPlanForm_active')
		delayField_input = self.selenium.find_element_by_id('DeliveryPlanForm_delayField')
		delayReason_input = self.selenium.find_element_by_id('DeliveryPlanForm_delayReason')
		submit = self.selenium.find_element_by_id('addDeliveryPlan_Submit')

		customerID_input.send_keys(object_customerID)
		deliveryDate_input.send_keys(object_deliveryDate)
		orderPlacedDate_input.send_keys(object_orderPlaced)
		invoiceNumber_input.send_keys(object_invoiceNumber)
		active_input.send_keys(object_active)
		delayField_input.send_keys(object_delayField)
		delayReason_input.send_keys(object_delayReason)

		submit.submit()
		# time.sleep(2)

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# OK ro refresh
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		print("def insert_DeliveryPlan -> complete")


	# Insert new raw material shortage
	def insert_RMShortage(self, rmShortage, rmLevel, rmStatus, date=None):

		# User clicks on addProductionNote_Toggle button to toggle form
		print("{}{}".format("addRawMaterial_Toggle:", self.selenium.find_element_by_id('addRawMaterial_Toggle')))
		self.selenium.find_element_by_id('addRawMaterial_Toggle').click()

		# User searches for inputs to name, email and date into input fields and submits information
		rmShortage_input = self.selenium.find_element_by_id('rmShortage_Form_rmShortage')
		rmLevel_input = self.selenium.find_element_by_id('rmShortage_Form_rmLevel')
		rmStatus_input = self.selenium.find_element_by_id('rmShortage_Form_rmStatus')

		# date_input = self.selenium.find_element_by_id('addObject_date')
		submit = self.selenium.find_element_by_id('add_RMShortageForm_Submit')

		rmShortage_input.send_keys(rmShortage)
		rmLevel_input.send_keys(rmLevel)
		rmStatus_input.send_keys(rmStatus)
		# date_input.send_keys(date)

		submit.submit()
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# Refresh message
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept() 

		print("def insert_RMShortage -> complete")

	# Edit existing raw material shortage
	def edit_RMShortage(self, rmShortage, rmLevel, rmStatus, date=None):

		# User clicks on addProductionNote_Toggle button to toggle form
		print("{}{}".format("addRawMaterial_Toggle:", self.selenium.find_element_by_id('addRawMaterial_Toggle')))
		self.selenium.find_element_by_id('editRawMaterial_Toggle').click()

		# User searches for inputs to name, email and date into input fields and submits information
		rmShortage_input = self.selenium.find_element_by_id('Edit_rmShortage_Form_rmShortage')
		rmLevel_input = self.selenium.find_element_by_id('Edit_rmShortage_Form_rmLevel')
		rmStatus_input = self.selenium.find_element_by_id('Edit_rmShortage_Form_rmStatus')

		# date_input = self.selenium.find_element_by_id('addObject_date')
		submit = self.selenium.find_element_by_id('edit_RMShortageForm_Submit')

		# Clear all fields and insert new Data
		rmLevel_input.clear()

		rmShortage_input.send_keys(rmShortage)
		rmLevel_input.send_keys(rmLevel)
		rmStatus_input.send_keys(rmStatus)
		# date_input.send_keys(date)

		submit.submit()

		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# Refresh message
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept() 

		print("def insert_RMShortage -> complete")

	# Insert new maintenance issue
	def insert_MaintenanceIssue(self, mIssue, mSubject, mStatus, mNote, date=None):

		# User clicks on addProductionNote_Toggle button to toggle form
		print("{}{}".format("addRawMaterial_Toggle:", self.selenium.find_element_by_id('addRawMaterial_Toggle')))
		self.selenium.find_element_by_id('addMaintenanceIssue_Toggle').click()

		# User searches for inputs to name, email and date into input fields and submits information
		mIssue_input = self.selenium.find_element_by_id('maintenanceIssue_Form_maintenanceType')
		mSubject_input = self.selenium.find_element_by_id('maintenanceIssue_Form_subject')
		mStatus_input = self.selenium.find_element_by_id('maintenanceIssue_Form_active')
		mNote_input = self.selenium.find_element_by_id('maintenanceIssue_Form_note')

		# date_input = self.selenium.find_element_by_id('addObject_date')
		submit = self.selenium.find_element_by_id('addMaintenanceIssue_Submit')

		mIssue_input.send_keys(mIssue)
		mSubject_input.send_keys(mSubject)
		mStatus_input.send_keys(mStatus)
		mNote_input.send_keys(mNote)

		# date_input.send_keys(date)

		submit.submit()
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# Refresh message
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept() 

		# # Refresh production list because refreshObject set to false
		# self.selenium.find_element_by_id('refreshProductionList').click()
		time.sleep(2)
		print("def insert_MaintenanceIssue -> complete")

	# Insert new maintenance issue
	def edit_MaintenanceIssue(self, mIssue, mSubject, mStatus, mNote, date=None):

		# User clicks on addProductionNote_Toggle button to toggle form
		self.selenium.find_element_by_id('editMaintenanceIssue_Toggle').click()

		# User searches for inputs to name, email and date into input fields and submits information
		mIssue_input = self.selenium.find_element_by_id('Edit_maintenanceIssue_Form_maintenanceType')
		mSubject_input = self.selenium.find_element_by_id('Edit_maintenanceIssue_Form_subject')
		mStatus_input = self.selenium.find_element_by_id('Edit_maintenanceIssue_Form_active')
		mNote_input = self.selenium.find_element_by_id('Edit_maintenanceIssue_Form_note')

		# date_input = self.selenium.find_element_by_id('addObject_date')
		submit = self.selenium.find_element_by_id('edit_MaintenanceIssue_Submit')

		# Clear all fields and insert new Data
		mSubject_input.clear()
		mNote_input.clear()

		mIssue_input.send_keys(mIssue)
		mSubject_input.send_keys(mSubject)
		mStatus_input.send_keys(mStatus)
		mNote_input.send_keys(mNote)

		# date_input.send_keys(date)

		submit.submit()

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# Refresh message
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept() 

		# # Refresh production list because refreshObject set to false
		# self.selenium.find_element_by_id('refreshProductionList').click()
		time.sleep(2)
		print("def insert_MaintenanceIssue -> complete")

	# Insert new production plan
	def insert_ProductionPlan(self, pPlan_machine, pPlan_BN, pPlan_description, pPlan_status, date=None):

		# User clicks on addProductionNote_Toggle button to toggle form
		print("{}{}".format("addProductionPlan_Toggle:", self.selenium.find_element_by_id('addProductionPlan_Toggle')))
		self.selenium.find_element_by_id('addProductionPlan_Toggle').click()

		# User searches for inputs to name, email and date into input fields and submits information
		pPlan_machine_input = self.selenium.find_element_by_id('ProductionPlan_Form_machine')
		pPlan_BN_input = self.selenium.find_element_by_id('ProductionPlan_Form_batchNumber')
		pPlan_description_input = self.selenium.find_element_by_id('ProductionPlan_Form_productDescription')
		pPlan_status_input = self.selenium.find_element_by_id('ProductionPlan_Form_status')

		# date_input = self.selenium.find_element_by_id('addObject_date')
		submit = self.selenium.find_element_by_id('addProductionPlan_Submit')

		pPlan_machine_input.send_keys(pPlan_machine)
		pPlan_BN_input.send_keys(pPlan_BN)
		pPlan_description_input.send_keys(pPlan_description)
		pPlan_status_input.send_keys(pPlan_status)

		# date_input.send_keys(date)
		submit.submit()

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# Refresh message
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept() 

		# # Refresh production list because refreshObject set to false
		# self.selenium.find_element_by_id('refreshProductionList').click()
		time.sleep(2)
		print("def insert_MaintenanceIssue -> complete")

	# edit existing production plan
	def edit_ProductionPlan(self, pPlan_machine, pPlan_BN, pPlan_description, pPlan_status, date=None):

		# User clicks on addProductionNote_Toggle button to toggle form
		self.selenium.find_element_by_id('editProductionPlan_Toggle').click()

		# User searches for inputs to name, email and date into input fields and submits information
		pPlan_machine_input = self.selenium.find_element_by_id('Edit_ProductionPlan_Form_machine')
		pPlan_BN_input = self.selenium.find_element_by_id('Edit_ProductionPlan_Form_batchNumber')
		pPlan_description_input = self.selenium.find_element_by_id('Edit_ProductionPlan_Form_productDescription')
		pPlan_status_input = self.selenium.find_element_by_id('Edit_ProductionPlan_Form_status')

		# date_input = self.selenium.find_element_by_id('addObject_date')
		submit = self.selenium.find_element_by_id('edit_ProductionPlan_Submit')

		# Clear all fields and insert new Data
		pPlan_description_input.clear()

		pPlan_machine_input.send_keys(pPlan_machine)
		pPlan_BN_input.send_keys(pPlan_BN)
		pPlan_description_input.send_keys(pPlan_description)
		pPlan_status_input.send_keys(pPlan_status)

		# date_input.send_keys(date)

		submit.submit()

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# Refresh message
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept() 

		# # Refresh production list because refreshObject set to false
		# self.selenium.find_element_by_id('refreshProductionList').click()
		time.sleep(2)
		print("def insert_MaintenanceIssue -> complete")

# Insert new production plan
	def insert_ProductType(self, productCode, productDescription, date=None):

		# User inserts product code and description
		productCode_input = self.selenium.find_element_by_id('ProductTypeForm_productCode')
		productDescription_input = self.selenium.find_element_by_id('ProductTypeForm_productDescription')

		# User types data and submits
		submit = self.selenium.find_element_by_id('addProductTypeForm_Submit')
		productCode_input.send_keys(productCode)
		productDescription_input.send_keys(productDescription)
		submit.submit()

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# Success message
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()
		time.sleep(2)
		print("def insert_ProductType -> complete")

# Insert new production plan
	def insert_Batch(self, paintInfoType, rdProject, productType, batchPeriod, batchNumber, date=None):

		# User inserts product code and description
		paintInfo_input = self.selenium.find_element_by_id('PaintInfoForm_paintInfoType')
		rdProject_input = self.selenium.find_element_by_id('PaintInfoForm_rdProject')
		productType_input = self.selenium.find_element_by_id('PaintInfoForm_productType')
		batchPeriod_input = self.selenium.find_element_by_id('PaintInfoForm_batchPeriod')
		batchNumber_input = self.selenium.find_element_by_id('PaintInfoForm_batchNumber')

		batch_input = self.selenium.find_element_by_id('ProductTypeForm_productDescription')

		# User types data and submits
		submit = self.selenium.find_element_by_id('addBatch_Submit')
		paintInfo_input.send_keys(paintInfoType)
		rdProject_input.send_keys(rdProject)
		productType_input.send_keys(productType)
		batchPeriod_input.send_keys(batchPeriod)
		batchNumber_input.send_keys(batchNumber)

		submit.submit()

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# Success message
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()
		time.sleep(2)

		print("def insert_Batch -> complete")

# Insert premix information
	def insert_premixInfo(self, premixDateIssued, premixInitialFog, premixInitialVisc, premixInitialViscUnit, premixDateLoaded, premixDatePremixPassed, premixFinalFOG, date=None):

		# User inserts product code and description
		premixDateIssued_input = self.selenium.find_element_by_id('Edit_PaintInfoForm_dateIssued')
		premixInitialFog_input = self.selenium.find_element_by_id('Edit_PaintInfoForm_initialFog')
		premixInitialVisc_input = self.selenium.find_element_by_id('Edit_PaintInfoForm_initialViscosity')
		premixInitialViscUnit_input = self.selenium.find_element_by_id('Edit_PaintInfoForm_initialViscosityUnit')
		premixDatePremixLoaded_input = self.selenium.find_element_by_id('Edit_PaintInfoForm_dateLoaded')
		premixDatePremixPassed_input = self.selenium.find_element_by_id('Edit_PaintInfoForm_datePremixPassed')
		premixFinalFOG_input = self.selenium.find_element_by_id('Edit_PaintInfoForm_finalFog')

		batch_input = self.selenium.find_element_by_id('ProductTypeForm_productDescription')

		# User types data and submits
		submit = self.selenium.find_element_by_id('addPremixInfo_Submit')
		premixDateIssued_input.send_keys(premixDateIssued)
		premixInitialFog_input.send_keys(premixInitialFog)
		premixInitialVisc_input.send_keys(premixInitialVisc)
		premixInitialViscUnit_input.send_keys(premixInitialViscUnit)
		premixDatePremixLoaded_input.send_keys(premixDateLoaded)
		premixDatePremixPassed_input.send_keys(premixDatePremixPassed)
		premixFinalFOG_input.send_keys(premixFinalFOG)

		submit.submit()

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# Server success
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()
		time.sleep(2)

		print("def insert_premixInfo -> complete")

# Insert new production plan
	def insert_BatchInfo(self, finalSg, finalOpacity, finalGloss, finalTouchDry, finalTouchDryUnit, finalHardDry, finalHardDryUnit, finalDFT, finalDFTUnit, finalViscosity, finalViscosityUnit, finalColorDe, finalColorDeSpec, date=None):

		print("finalSg: {}".format(finalSg))
		# User identifies fields
		finalSg_input = self.selenium.find_element_by_id('Edit_BatchInfoForm_finalSg')
		finalOpacity_input = self.selenium.find_element_by_id('Edit_BatchInfoForm_finalOpacity')
		finalGloss_input = self.selenium.find_element_by_id('Edit_BatchInfoForm_finalGloss')
		finalTouchDry_input = self.selenium.find_element_by_id('Edit_BatchInfoForm_finalTouchDry')
		finalTouchDryUnit_input = self.selenium.find_element_by_id('Edit_BatchInfoForm_finalTouchDryUnit')
		finalHardDry_input = self.selenium.find_element_by_id('Edit_BatchInfoForm_finalHardDry')
		finalHardDryUnit_input = self.selenium.find_element_by_id('Edit_BatchInfoForm_finalHardDryUnit')
		finalDFT_input = self.selenium.find_element_by_id('Edit_BatchInfoForm_finalDft')
		finalDFTUnit_input = self.selenium.find_element_by_id('Edit_BatchInfoForm_finalDftUnit')
		finalViscosity_input = self.selenium.find_element_by_id('Edit_BatchInfoForm_finalViscosity')
		finalViscosityUnit_input = self.selenium.find_element_by_id('Edit_BatchInfoForm_finalViscosityUnit')
		finalColorDe_input = self.selenium.find_element_by_id('Edit_BatchInfoForm_finalColorDe')
		finalColorDeSpec_input = self.selenium.find_element_by_id('Edit_BatchInfoForm_finalColorDeSpec')
		submit = self.selenium.find_element_by_id('addBatchInfo_Submit')

		# User types data and submits
		finalSg_input.send_keys(finalSg)
		finalOpacity_input.send_keys(finalOpacity)
		finalGloss_input.send_keys(finalGloss)
		finalTouchDry_input.send_keys(finalTouchDry)
		finalTouchDryUnit_input.send_keys(finalTouchDryUnit)
		finalHardDry_input.send_keys(finalHardDry)
		finalHardDryUnit_input.send_keys(finalHardDryUnit)
		finalDFT_input.send_keys(finalDFT)
		finalDFTUnit_input.send_keys(finalDFTUnit)
		finalViscosity_input.send_keys(finalViscosity)
		finalViscosityUnit_input.send_keys(finalViscosityUnit)
		finalColorDe_input.send_keys(finalColorDe)
		finalColorDeSpec_input.send_keys(finalColorDeSpec)
		
		submit.submit()

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# Success message
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()
		time.sleep(5)

		print("def insert_BatchInfo -> complete")

# Insert new production plan
	def insert_BatchAdjustment(self, rm, adjustAmount, adjustmentUnit):

		# User identifies fields
		rm_input = self.selenium.find_element_by_id('BatchAdjustmentForm_rmCode')
		adjustAmount_input = self.selenium.find_element_by_id('BatchAdjustmentForm_adjustmentAmount')
		adjustmentUnit_input = self.selenium.find_element_by_id('BatchAdjustmentForm_adjustmentUnit')
		submit = self.selenium.find_element_by_id('addFinishingAdjustment_Submit')

		# User types data and submits
		rm_input.send_keys(rm)
		adjustAmount_input.send_keys(adjustAmount)
		adjustmentUnit_input.send_keys(adjustmentUnit)
		
		submit.submit()

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# Success message
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()
		time.sleep(5)

		print("def insert_BatchAdjustment -> complete")

# Edit batch adjustment
	def edit_BatchAdjustment(self, adjustAmount, adjustmentUnit):

		# User identifies fields
		# rm_input = self.selenium.find_element_by_id('Edit_BatchAdjustmentForm_rmCode')
		adjustAmount_input = self.selenium.find_element_by_id('Edit_BatchAdjustmentForm_adjustmentAmount')
		adjustmentUnit_input = self.selenium.find_element_by_id('Edit_BatchAdjustmentForm_adjustmentUnit')
		submit = self.selenium.find_element_by_id('addBatchAdjustment_Submit')

		# User clears old fields types data and submits
		adjustAmount_input.clear()
		adjustAmount_input.send_keys(adjustAmount)
		adjustmentUnit_input.send_keys(adjustmentUnit)
		
		submit.submit()

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# refresh
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()
		time.sleep(5)

		print("def edit_BatchAdjustment -> complete")

# Edit RD Project
	def edit_RDProject(self, customer, subject, instructions):

		# User identifies fields
		customer_input = self.selenium.find_element_by_id('Edit_RDProject_customer')
		subject_input = self.selenium.find_element_by_id('Edit_RDProject_subject')
		instructions_input = self.selenium.find_element_by_id('Edit_RDProject_instructions')
		submit = self.selenium.find_element_by_id('editRDProject_Submit')

		# User clears old fields types data and submits
		customer_input.send_keys(customer)
		subject_input.send_keys(subject)
		instructions_input.send_keys(instructions)

		submit.submit()

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# refresh
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()
		time.sleep(5)

		print("def edit_RDProject -> complete")

# Edit RD Project
	def edit_ProductType(self, productCode, productDescription):

		# User identifies fields
		productCode_input = self.selenium.find_element_by_id('Edit_ProductType_productCode')
		productDescription_input = self.selenium.find_element_by_id('Edit_ProductType_productDescription')
		submit = self.selenium.find_element_by_id('editProductType_Submit')

		# User clears old fields types data and submits
		productCode_input.clear()
		productDescription_input.clear()

		productCode_input.send_keys(productCode)
		productDescription_input.send_keys(productDescription)

		submit.submit()

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# refresh
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()
		time.sleep(5)

		print("def edit_RDProject -> complete")