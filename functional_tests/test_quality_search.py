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
from quality.models import ProductType, RDProject
from sales.models import CustomerID
from production.models import RMReference
import time


# StaticLiveServerTestCase -> serve static files during test, spin up development server for test, creates and deletes test database without interfering with production database
class TestEditDeleteObject(FunctionalTest):

	def test_1_editDelete_ProductType_RDPlan_BatchCard_All(self):
		# Create reference objects
		ProductType(productCode="z1234", productDescription="testNewProductType").save()
		ProductType(productCode="z4567", productDescription="second_testNewProductType").save()
		CustomerID(
			customerCode="101",
			customerName="testCustomerName",
			procurementName="procurementName",
			procurementWorkNum="procurementWorkNum",
			procurementWorkEmail="procurementWorkEmail@vibes.com").save()
		CustomerID(
			customerCode="102",
			customerName="second_testCustomerName",
			procurementName="procurementName",
			procurementWorkNum="procurementWorkNum",
			procurementWorkEmail="procurementWorkEmail@vibes.com").save()
		RDProject(
			subject="Test R&D Project",
			customer=CustomerID.objects.latest('id')).save()
		RDProject(
			subject="Test second R&D Project",
			customer=CustomerID.objects.latest('id')).save()
		RMReference(
			rmCode="S101",
			rmDescription="someRMAdjustment",
			).save()

		# Web request
		self.selenium.get( ('%s%s' % (self.live_server_url, '/')) )
		self.wait_for_(lambda: self.find_object_by_id("updateItem", "ajax loaded."))

		# User searches for a batch card - by status
		self.selenium.find_element_by_id('addQuality').click() 
		time.sleep(1) 
		self.selenium.find_element_by_id('InserBatch_heading').click()
		self.insert_Batch(
			'Batch',
			'Test R&D Project',
			'z1234 testNewProductType',
			201,
			12345
			)

		# # refresh
		# self.alert_wait()
		# alertObj = self.selenium.switch_to.alert
		# alertObj.accept()
		# time.sleep(5)

		self.wait_for_(lambda: self.find_object_by_id("QualityObject_subject", "201 - 12345"))
		self.selenium.find_element_by_id('searchQuality').click()
		self.wait_for_(lambda: self.find_object_by_id("searchBatchCards", "Search batch cards"))
		self.selenium.find_element_by_id('searchBatchCards').click()
		time.sleep(1)
		# Test for in progress batch cards
		
		self.selenium.find_element_by_id('rad_batchStatus').click()
		self.selenium.find_element_by_id('search_Quality_Field').send_keys("In Progress")
		self.selenium.find_element_by_id('searchQualityPlan_submit').submit()
		self.closeNotifications()
		self.selenium.execute_script("window.scrollTo(0, 1900)")
		time.sleep(3)
		self.wait_for_(lambda: self.find_object_by_id("QualityObject_subject", "201 - 12345"))

		# Complete batch and retest - expect no data
		self.selenium.execute_script("window.scrollTo(0, 2200)")
		self.selenium.find_element_by_id('confirmUpdateQualityObject_Toggle').click()
		self.selenium.find_element_by_xpath('//span[@ajaxStatus="updateQualityPlan"]').click()
		self.closeNotifications()
		self.selenium.execute_script("window.scrollTo(0, 1900)")
		self.selenium.find_element_by_id('refreshQualityPlanList').click()
		self.closeNotifications()
		self.selenium.execute_script("window.scrollTo(0, 2100)")
		time.sleep(3)
		self.selenium.find_element_by_id('rad_batchStatus').click()
		self.selenium.find_element_by_id('search_Quality_Field').clear()
		self.selenium.find_element_by_id('search_Quality_Field').send_keys("In Progress")
		self.selenium.find_element_by_id('searchQualityPlan_submit').submit()
		self.closeNotifications()
		self.selenium.execute_script("window.scrollTo(0, 2100)")
		time.sleep(3)
		self.wait_for_(lambda: self.find_object_by_id("noDataQualityObject", "No data here!"))

		# Search by compelted batch cards
		self.selenium.find_element_by_id('rad_batchStatus').click()
		self.selenium.find_element_by_id('search_Quality_Field').clear()
		self.selenium.find_element_by_id('search_Quality_Field').send_keys("Completed")
		self.selenium.find_element_by_id('searchQualityPlan_submit').submit()
		self.closeNotifications()
		self.selenium.execute_script("window.scrollTo(0, 2100)")
		time.sleep(3)
		self.wait_for_(lambda: self.find_object_by_id("QualityObject_subject", "201 - 12345"))

		# Search by ProductType - Expect No Data
		self.selenium.find_element_by_id('rad_productType').click()
		self.selenium.find_element_by_id('search_Quality_Field').clear()
		self.selenium.find_element_by_id('search_Quality_Field').send_keys("z4567")
		self.selenium.find_element_by_id('searchQualityPlan_submit').submit()
		self.closeNotifications()
		self.selenium.execute_script("window.scrollTo(0, 2100)")
		time.sleep(3)
		self.wait_for_(lambda: self.find_object_by_id("noDataQualityObject", "No data here!"))

		# Search by ProductType - Expect Data
		self.selenium.find_element_by_id('rad_productType').click()
		self.selenium.find_element_by_id('search_Quality_Field').clear()
		self.selenium.find_element_by_id('search_Quality_Field').send_keys("testNewProductType")
		self.selenium.find_element_by_id('searchQualityPlan_submit').submit()
		self.closeNotifications()
		self.selenium.execute_script("window.scrollTo(0, 2100)")
		time.sleep(3)
		self.wait_for_(lambda: self.find_object_by_id("QualityObject_subject", "201 - 12345"))

		# Search by ProductCode - Expect No Data 
		self.selenium.find_element_by_id('rad_productCode').click()
		self.selenium.find_element_by_id('searchQualityPlan_submit').submit()
		self.closeNotifications()
		self.selenium.execute_script("window.scrollTo(0, 2100)")
		time.sleep(3)
		self.wait_for_(lambda: self.find_object_by_id("noDataQualityObject", "No data here!"))

		# Search by ProductCode - Expect Data
		self.selenium.find_element_by_id('rad_productCode').click()
		self.selenium.find_element_by_id('search_Quality_Field').clear()
		self.selenium.find_element_by_id('search_Quality_Field').send_keys("z1234")
		self.selenium.find_element_by_id('searchQualityPlan_submit').submit()
		self.closeNotifications()
		self.selenium.execute_script("window.scrollTo(0, 2100)")
		time.sleep(3)
		self.wait_for_(lambda: self.find_object_by_id("QualityObject_subject", "201 - 12345"))

		# Search by BatchNumber - Expect No Data 
		self.selenium.find_element_by_id('rad_batchNumber').click()
		self.selenium.find_element_by_id('search_Quality_Field').clear()
		self.selenium.find_element_by_id('search_Quality_Field').send_keys("vibes")
		self.selenium.find_element_by_id('searchQualityPlan_submit').submit()
		self.closeNotifications()
		self.selenium.execute_script("window.scrollTo(0, 2100)")
		time.sleep(3)
		self.wait_for_(lambda: self.find_object_by_id("noDataQualityObject", "No data here!"))

		# Search by BatchNumber - Expect Data
		self.selenium.find_element_by_id('rad_batchNumber').click()
		self.selenium.find_element_by_id('search_Quality_Field').clear()
		self.selenium.find_element_by_id('search_Quality_Field').send_keys("12345")
		self.selenium.find_element_by_id('searchQualityPlan_submit').submit()
		self.closeNotifications()
		self.selenium.execute_script("window.scrollTo(0, 2100)")
		time.sleep(3)
		self.wait_for_(lambda: self.find_object_by_id("QualityObject_subject", "201 - 12345"))

		# Search by Lab Project by Customer - Expect No Data 
		self.selenium.find_element_by_id('rad_rdProject').click()
		self.selenium.find_element_by_id('search_Quality_Field').clear()
		self.selenium.find_element_by_id('search_Quality_Field').send_keys("vibes")
		self.selenium.find_element_by_id('searchQualityPlan_submit').submit()
		self.closeNotifications()
		self.selenium.execute_script("window.scrollTo(0, 2100)")
		time.sleep(3)
		self.wait_for_(lambda: self.find_object_by_id("noDataQualityObject", "No data here!"))

		# Search by Lab Project by Customer - Expect Data
		self.selenium.find_element_by_id('rad_rdProject').click()
		self.selenium.find_element_by_id('search_Quality_Field').clear()
		self.selenium.find_element_by_id('search_Quality_Field').send_keys("testCustomerName")
		self.selenium.find_element_by_id('searchQualityPlan_submit').submit()
		self.closeNotifications()
		self.selenium.execute_script("window.scrollTo(0, 2100)")
		time.sleep(3)
		self.wait_for_(lambda: self.find_object_by_id("QualityObject_subject", "201 - 12345"))

		print("\nTEST: def test_1_editDelete_ProductType_RDPlan_BatchCard_All -> complete\n")
		return False

