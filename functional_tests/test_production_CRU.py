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
from production.models import RMReference
from django.contrib.auth.models import User
import time


# StaticLiveServerTestCase -> serve static files during test, spin up development server for test, creates and deletes test database without interfering with production database
class TestEditDeleteObject(FunctionalTest):
	# # Generic search for a Production Meeting
	# def wait(fn):
	# 	def modifiedWait(*args, **kwargs):
	# 		startTime = time.time()
	# 		# run the loop until function meets specification
	# 		while True:
	# 			try:
	# 				return fn(*args, **kwargs)
	# 			except (AssertionError, WebDriverException) as e:
	# 				# If the browser has exceeded a 10 second response time, raise and exception
	# 				if time.time() - startTime > self.MAX_WAIT:
	# 					raise e				
	# 				time.sleep(0.5)		
	# 	return modifiedWait	

	def test_1_editDelete_ProductionMeeting_All(self):
		User.objects.create_user('admin', 'admin@testuser.com', 'adminTest')
		RMReference.objects.create(rmCode="101", rmDescription="testRMReference_1", rmWarningLevel=1201).save()
		RMReference.objects.create(rmCode="102", rmDescription="testRMReference_2", rmWarningLevel=1201).save()
		
		# Web request
		self.selenium.get( ('%s%s' % (self.live_server_url, '/')) )
		self.wait_for_(lambda: self.find_object_by_id("loginHeader", "Welcome to Marindec."))
		self.insert_Login(
			"admin", 
			"adminTest",
			)

		self.wait_for_(lambda: self.find_object_by_id("updateItem", "ajax loaded."))

		# User submits production meeting and waits for it to upload on the productionMeeting_subject
		self.insert_ProductionMeeting(
			"New Prod Meeting.",
			# datetime.strftime(date.today(), '%Y-%m-%d'),
			)	
		# Success message and verification
		# self.wait_for_(lambda: self.find_object_by_id("notification", "New production meeting created!"))
		self.wait_for_(lambda: self.find_object_by_id("productionMeeting_subject", "New Prod Meeting."))

		time.sleep(1)
		# User clicks on editProductionMeeting to change subject of production meeting, refreshes and confirms change
		self.edit_ProductionMeeting(
			"Edit Prod Meeting.",
			# datetime.strftime(date.today(), '%Y-%m-%d'),
			)	

		# Success message and verification
		# self.wait_for_(lambda: self.find_object_by_id("notification", "Subject of meeting edited successfully!"))
		self.wait_for_(lambda: self.find_object_by_id("productionMeeting_subject", "Edit Prod Meeting."))
		time.sleep(1)

		# User clicks on productionMeeting_subject to expand production notes
		self.selenium.find_element_by_id('productionMeeting_subject').click()
		self.wait_for_(lambda: self.find_object_by_id("productionMeeting_heading1", "General production notes"))

		# User clicks on productionMeeting_heading1 to expand General production notes
		self.selenium.find_element_by_id('productionMeeting_heading1').click()
		self.wait_for_(lambda: self.find_object_by_id("addProductionNote_Toggle", "Insert a production note"))

		# User clicks in addProductionNote_Toggle to expand form and insert new general production note
		self.insert_ProductionNote(
			"New Prod Note.",
			# datetime.strftime(date.today(), '%Y-%m-%d'),
			)
		# Success message and verification
		# self.wait_for_(lambda: self.find_object_by_id("notification", "Production note created successfully!"))
		time.sleep(1)

		# User clicks on productionMeeting_subject to expand production meeting
		self.wait_for_(lambda: self.find_object_by_id("productionMeeting_subject", "Edit Prod Meeting."))
		self.selenium.find_element_by_id('productionMeeting_subject').click()
		self.selenium.find_element_by_id('productionMeeting_heading1').click()
		self.wait_for_(lambda: self.find_object_by_id("productioNote_1", "New Prod Note."))

		# User clicks editProductionNote_Toggle to edit productio note
		self.edit_ProductionNote(
			"Edit Prod Note.",
			# datetime.strftime(date.today(), '%Y-%m-%d'),
			)

		# User clicks on productionMeeting_subject to expand production meeting
		time.sleep(1)
		self.wait_for_(lambda: self.find_object_by_id("productionMeeting_subject", "Edit Prod Meeting."))
		self.selenium.find_element_by_id('productionMeeting_subject').click()
		self.selenium.find_element_by_id('productionMeeting_heading1').click()
		# Success message and verification
		# self.wait_for_(lambda: self.find_object_by_id("notification", "Production note edited successfully!"))
		self.wait_for_(lambda: self.find_object_by_id("productioNote_1", "Edit Prod Note."))
		time.sleep(1)

		# User clicks on productionMeeting_heading1 to expand Raw Material Shortages
		self.selenium.find_element_by_id('productionMeeting_heading2').click()
		self.wait_for_(lambda: self.find_object_by_id("addRawMaterial_Toggle", "Insert a raw material shortage"))

		# User inserts RMShortage, refreshes and checks to see if updated on Production List
		self.insert_RMShortage(
			"101:testRMReference_1",
			2306,
			"Caution",
			# datetime.strftime(date.today(), '%Y-%m-%d'),
			)	
		
		# User clicks on productionMeeting_subject to expand production meeting
		time.sleep(1)
		self.wait_for_(lambda: self.find_object_by_id("productionMeeting_subject", "Edit Prod Meeting."))
		self.selenium.find_element_by_id('productionMeeting_subject').click()
		self.selenium.find_element_by_id('productionMeeting_heading2').click()
		# Success message and verification
		# self.wait_for_(lambda: self.find_object_by_id("notification", "Raw material shortage created successfully!"))
		self.wait_for_(lambda: self.find_object_by_id("rmShortage_1_Meeting_1", "101: testRMReference_1 at 2306"))
		time.sleep(1)

		# User clicks editRawMaterial_Toggle to edit raw material shortage
		self.edit_RMShortage(
			"102:testRMReference_2",
			2306,
			"Caution",
			# datetime.strftime(date.today(), '%Y-%m-%d'),
			)	

		# User clicks on productionMeeting_subject to expand production meeting
		time.sleep(1)
		self.wait_for_(lambda: self.find_object_by_id("productionMeeting_subject", "Edit Prod Meeting."))
		self.selenium.find_element_by_id('productionMeeting_subject').click()
		self.selenium.find_element_by_id('productionMeeting_heading2').click()
		# Success message and verification
		# self.wait_for_(lambda: self.find_object_by_id("notification", "Raw material shortage changed successfully!"))
		self.wait_for_(lambda: self.find_object_by_id("rmShortage_1_Meeting_1", "102: testRMReference_2 at 2306"))
		time.sleep(1)

		# User clicks on productionMeeting_heading3 to expand maintenance issues
		self.selenium.find_element_by_id('productionMeeting_heading3').click()
		self.wait_for_(lambda: self.find_object_by_id("addMaintenanceIssue_Toggle", "Insert a maintenance issue"))

		# User inserts MaintenanceIssue, refreshes and checks to see if updated on Production List
		self.selenium.find_element_by_id('addMaintenanceIssue_Toggle').click()
		self.insert_MaintenanceIssue(
			"Other",
			"testMaintenanceIssue",
			"Unresolved",
			"testMaintenanceNote"
			# datetime.strftime(date.today(), '%Y-%m-%d'),
			)
		
		time.sleep(1)
		# Success message and verification
		# self.wait_for_(lambda: self.find_object_by_id("notification", "Maintenance issue created successfully!"))
		time.sleep(1)
		self.selenium.find_element_by_id('productionMeeting_subject').click()
		self.selenium.find_element_by_id('productionMeeting_heading3').click()
		self.wait_for_(lambda: self.find_object_by_id("maintenanceIssueSubject_1", "testMaintenanceIssue"))

		# User clicks editRawMaterial_Toggle to edit raw material shortage
		self.edit_MaintenanceIssue(
			"Other",
			"editMaintenanceIssue",
			"Unresolved",
			"editMaintenanceNote"
			# datetime.strftime(date.today(), '%Y-%m-%d'),
			)
		time.sleep(1)
		# Success message and verification
		# self.wait_for_(lambda: self.find_object_by_id("notification", "Maintenance issue edited successfully!"))
		time.sleep(1)

		self.selenium.find_element_by_id('productionMeeting_subject').click()
		self.selenium.find_element_by_id('productionMeeting_heading3').click()
		self.wait_for_(lambda: self.find_object_by_id("maintenanceIssueSubject_1", "editMaintenanceIssue"))

		# User clicks on productionMeeting_heading4 to expand production plan
		self.selenium.find_element_by_id('productionMeeting_heading4').click()
		self.wait_for_(lambda: self.find_object_by_id("addProductionPlan_Toggle", "Insert a production plan"))

		# User inserts MaintenanceIssue, refreshes and checks to see if updated on Production List
		self.insert_ProductionPlan(
			"BM1",
			"219/35487",
			"testProductionPlan",
			"To Load"
			# datetime.strftime(date.today(), '%Y-%m-%d'),
			)
		
		time.sleep(1)
		# Success message and verification
		# self.wait_for_(lambda: self.find_object_by_id("notification", "Production plan created successfully!"))
		time.sleep(1)

		self.selenium.find_element_by_id('productionMeeting_subject').click()
		self.selenium.find_element_by_id('productionMeeting_heading4').click()
		self.wait_for_(lambda: self.find_object_by_id("pPlanMachine_1", "BM1 - testProductionPlan"))

		# User clicks editProductionPlan_Toggle to edit production plan
		self.edit_ProductionPlan(
			"BM1",
			"219/35487",
			"editProductionPlan",
			"To Load"
			# datetime.strftime(date.today(), '%Y-%m-%d'),
			)

		# Production meeting deleted succesfully!
		# Production note deleted succesfully!
		# Raw material shortage deleted succesfully!
		# Maintenance form deleted succesfully!
		# Production plan deleted succesfully!

		time.sleep(1)
		# Success message and verification
		# self.wait_for_(lambda: self.find_object_by_id("notification", "Production plan edited successfully!"))
		time.sleep(1)
		self.selenium.find_element_by_id('productionMeeting_subject').click()
		self.selenium.find_element_by_id('productionMeeting_heading4').click()
		time.sleep(1)
		self.wait_for_(lambda: self.find_object_by_id("pPlanMachine_1", "BM1 - editProductionPlan"))

		# User begins to delete information
		self.selenium.find_element_by_id('refreshProductionList').click()

		# User looks for editProductionPlan, deletes production plan and checs
		time.sleep(1)
		self.wait_for_(lambda: self.find_object_by_id("productionMeeting_subject", "Edit Prod Meeting."))
		self.selenium.find_element_by_id('productionMeeting_subject').click()
		self.selenium.find_element_by_id('productionMeeting_heading4').click()
		time.sleep(2)
		# self.wait_for_(lambda: self.find_object_by_id("pPlanMachine_1", "BM1 - editProductionPlan"))
		self.selenium.find_element_by_id('deleteProductionPlan_Toggle').click()
		self.selenium.find_element_by_xpath('//span[@ajaxStatus="deleteProductionPlanForm"]').click()
		# self.wait_for_(lambda: self.find_object_by_id("notification", "Production plan deleted succesfully!"))
		time.sleep(1)

		# User looks for editMaintenanceIssue, deletes maintenance issue and checs
		self.selenium.find_element_by_id('productionMeeting_heading3').click()
		# self.wait_for_(lambda: self.find_object_by_id("maintenanceIssueSubject_1", "editMaintenanceIssue"))
		self.selenium.find_element_by_id('deleteMaintenanceIssue_Toggle').click()
		self.selenium.find_element_by_xpath('//span[@ajaxStatus="deleteMaintenanceIssueForm"]').click()
		# self.wait_for_(lambda: self.find_object_by_id("notification", "Maintenance form deleted succesfully!"))
		time.sleep(1)

		# User looks for testRMReference_2, deletes rm shortage and checs
		self.selenium.find_element_by_id('productionMeeting_heading2').click()
		# self.wait_for_(lambda: self.find_object_by_id("rmShortage_1_Meeting_1", "102: testRMReference_2 at 2306"))
		self.selenium.find_element_by_id('deleteRMShortage_Toggle').click()
		self.selenium.find_element_by_xpath('//span[@ajaxStatus="deleteRMShortageForm"]').click()
		# self.wait_for_(lambda: self.find_object_by_id("notification", "Raw material shortage deleted succesfully!"))
		time.sleep(1)

		# User looks for "Edit Prod Note.", deletes production note and checs
		self.selenium.find_element_by_id('productionMeeting_heading1').click()
		# self.wait_for_(lambda: self.find_object_by_id("productioNote_1", "Edit Prod Note."))
		self.selenium.find_element_by_id('deleteProductionNote_Toggle').click()
		self.selenium.find_element_by_xpath('//span[@ajaxStatus="deleteProductionNote"]').click()
		# self.wait_for_(lambda: self.find_object_by_id("notification", "Production note deleted succesfully!"))
		time.sleep(1)

		# User looks for "Edit Prod Note.", deletes production note and checs
		self.selenium.find_element_by_id('deleteProductionMeeting_Toggle').click()
		# self.selenium.find_element_by_id('deleteProductionMeeting_Toggle').click()
		self.selenium.find_element_by_xpath('//span[@ajaxStatus="deleteProductionMeetingForm"]').click()
		# self.wait_for_(lambda: self.find_object_by_id("notification", "Production meeting deleted succesfully!"))
		time.sleep(1)

		print("\ndef:test_1_editDelete_ProductionMeeting_All -> complete\n")

		return False

