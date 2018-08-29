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
from django.contrib.auth.models import User
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
			customer=CustomerID.objects.get(customerName="testCustomerName")).save()
		RDProject(
			subject="Test second R&D Project",
			customer=CustomerID.objects.get(customerName="second_testCustomerName")).save()
		RMReference(
			rmCode="S101",
			rmDescription="someRMAdjustment",
			).save()

		User.objects.create_user('admin', 'admin@testuser.com', 'adminTest')
		# Web request
		self.selenium.get( ('%s%s' % (self.live_server_url, '/')) )
		self.wait_for_(lambda: self.find_object_by_id("loginHeader", "Welcome to Marindec."))
		self.insert_Login(
			"admin", 
			"adminTest",
			)
		self.wait_for_(lambda: self.find_object_by_id("updateItem", "ajax loaded."))

		# User toggles addQuality to insert a new batch, and checks to see that it reflects on page
		self.selenium.find_element_by_id('addQuality').click() 
		time.sleep(1) 
		self.selenium.find_element_by_id('InserBatch_heading').click()
		self.insert_Batch(
			'Batch',
			'second_testCustomerName',
			'z1234 testNewProductType',
			201,
			12345
			)
		self.wait_for_(lambda: self.find_object_by_id("QualityObject_subject", "201 - 12345"))

		# User clicks on quality object to start inserting premix, batch and finishing adjustments. User also checks to see that labels are updated accordingly
		self.selenium.find_element_by_id('QualityObject_subject').click()
		time.sleep(1) 
		self.selenium.find_element_by_id('qualityPlan_heading1').click()
		time.sleep(1)
		self.selenium.find_element_by_id('editPremixInfo').click()
		self.insert_premixInfo(
			'2018-02-01',
			120,
			80,
			"KU",
			'2018-02-01',
			'2018-02-04',
			1,
			)

		time.sleep(2)

		self.wait_for_(lambda: self.find_object_by_id("QualityObject_subject", "201 - 12345"))
		self.selenium.find_element_by_id('QualityObject_subject').click()
		time.sleep(1) 
		self.selenium.find_element_by_id('qualityPlan_heading1').click()
		time.sleep(1)

		self.wait_for_(lambda: self.find_object_by_id("dateIssued_1", "Feb. 1, 2018"))
		self.wait_for_(lambda: self.find_object_by_id("dateLoaded_1", "Feb. 1, 2018"))
		self.wait_for_(lambda: self.find_object_by_id("datePremixPass_1", "Feb. 4, 2018"))
		self.wait_for_(lambda: self.find_object_by_id("initialPremixFOG_1", "120.0 um"))
		self.wait_for_(lambda: self.find_object_by_id("initialVisc_1", "80.0 KU"))
		self.wait_for_(lambda: self.find_object_by_id("finaPremixFOG_1", "1.0 um"))

		# User clicks on qualityPlan_heading2, Batch Parameters, to start inserting batch Parameters. User also checks to see that labels are updated accordingly
		self.selenium.find_element_by_id('qualityPlan_heading2').click()
		time.sleep(1)
		self.selenium.find_element_by_id('editBatchInfo').click()
		time.sleep(1)
		self.insert_BatchInfo(
			"0.96",
			"99.43",
			"76",
			"30",
			"Min",
			"90",
			"Min",
			"30",
			"200um",
			"60",
			"KU",
			"0.25",
			"Spectrophotometer",
			)

		# # refresh accept
		# self.alert_wait()
		# alertObj = self.selenium.switch_to.alert
		# alertObj.accept()

		time.sleep(2)

		self.wait_for_(lambda: self.find_object_by_id("QualityObject_subject", "201 - 12345"))
		self.selenium.find_element_by_id('QualityObject_subject').click()
		time.sleep(1)
		self.selenium.find_element_by_id('qualityPlan_heading2').click()
		time.sleep(1)
		self.wait_for_(lambda: self.find_object_by_id("finalSg_1", "0.96 ml/g (L/Kg)"))
		self.wait_for_(lambda: self.find_object_by_id("finalTouchDry_1", "30.0 Min"))
		self.wait_for_(lambda: self.find_object_by_id("finalHardDry_1", "90.0 Min"))
		self.wait_for_(lambda: self.find_object_by_id("finalDFT_1", "30.0um on WFT of 200um"))
		self.wait_for_(lambda: self.find_object_by_id("finalViscosity_1", "60.0 KU"))
		self.wait_for_(lambda: self.find_object_by_id("finalOpacity_1", "99.43"))
		self.wait_for_(lambda: self.find_object_by_id("finalGloss_1", "76.0"))
		self.wait_for_(lambda: self.find_object_by_id("finalColorDE_1", "0.25 on Spectrophotometer"))

		# User clicks on qualityPlan_heading3, Finishing Adjustments, to start inserting finishing adjustments. User also checks to see that labels are updated accordingly
		self.selenium.find_element_by_id('qualityPlan_heading3').click()
		time.sleep(1)
		self.selenium.find_element_by_id('addBatchAdjustment_Toggle').click()
		time.sleep(1)
		self.insert_BatchAdjustment(
			"S101: someRMAdjustment",
			"101.5",
			"Litre",
			)

		# # refresh accept
		# self.alert_wait()
		# alertObj = self.selenium.switch_to.alert
		# alertObj.accept()

		# time.sleep(2)

		self.wait_for_(lambda: self.find_object_by_id("QualityObject_subject", "201 - 12345"))
		self.selenium.find_element_by_id('QualityObject_subject').click()
		time.sleep(1)
		self.selenium.find_element_by_id('qualityPlan_heading3').click()
		time.sleep(1)
		self.wait_for_(lambda: self.find_object_by_id("adjustmentRMCode_1", "S101: someRMAdjustment"))
		self.wait_for_(lambda: self.find_object_by_id("adjustmentAmount_1", "101.5 Litre"))

		# User made a mistake and wants to change adjustment amount
		self.selenium.find_element_by_id('editBatchAdjustment').click()
		self.edit_BatchAdjustment(
			"110",
			"Kg"
			)

		# # refresh accept
		# self.alert_wait()
		# alertObj = self.selenium.switch_to.alert
		# alertObj.accept()
		time.sleep(2)

		self.wait_for_(lambda: self.find_object_by_id("QualityObject_subject", "201 - 12345"))
		self.selenium.find_element_by_id('QualityObject_subject').click()
		time.sleep(1)
		self.selenium.find_element_by_id('qualityPlan_heading3').click()
		time.sleep(1)
		self.wait_for_(lambda: self.find_object_by_id("adjustmentRMCode_1", "S101: someRMAdjustment"))
		self.wait_for_(lambda: self.find_object_by_id("adjustmentAmount_1", "110 Kg"))
		self.selenium.find_element_by_id('refreshQualityPlanList').click()
		self.closeNotifications()
		time.sleep(3)

		# User decides to edit an RDPRoject
		self.selenium.find_element_by_id('addQuality').click() 
		time.sleep(1) 
		self.selenium.find_element_by_id('editRDProject_heading').click()
		self.selenium.find_element_by_id('searchQRDProjectInput').send_keys("testCustomerName")
		self.selenium.find_element_by_id('searchRDProject_Submit').submit()
		self.closeNotifications()
		self.wait_for_(lambda: self.find_object_by_id("rdProjectSearchResult_subject", "Test R&D Project"))
		self.selenium.execute_script("window.scrollTo(0, 2200)")
		self.selenium.find_element_by_id('editRDProject_Toggle').click()
		self.wait_for_(lambda: self.find_object_by_id("editRDProject_intro", "Edit this R&D Project"))
		self.edit_RDProject(
			"testCustomerName",
			"TDS for Alan",
			"Fix volume solids and spreading rate")

		# # refresh accept
		# self.alert_wait()
		# alertObj = self.selenium.switch_to.alert
		# alertObj.accept()
		time.sleep(2)

		self.wait_for_(lambda: self.find_object_by_id("QualityObject_subject", "201 - 12345"))

		# User decides to delete an RD Project - All Batch Cards with corresponding RD projects must get removed as well
		self.selenium.find_element_by_id('addQuality').click() 
		time.sleep(1) 
		self.selenium.find_element_by_id('editRDProject_heading').click()
		self.selenium.find_element_by_id('searchQRDProjectInput').clear()
		self.selenium.find_element_by_id('searchQRDProjectInput').send_keys("testCustomerName")
		self.selenium.find_element_by_id('searchRDProject_Submit').submit()
		time.sleep(1)
		self.closeNotifications()
		time.sleep(5)
		self.selenium.find_element_by_id('deleteRDProject_Toggle').click()
		self.selenium.find_element_by_xpath('//span[@ajaxStatus="deleteRDProjectForm"]').click()

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# # refresh
		# self.alert_wait()
		# alertObj = self.selenium.switch_to.alert
		# alertObj.accept()
		# time.sleep(5)
		
		self.wait_for_(lambda: self.find_object_by_id("noDataQualityObject", "No data here!"))

		# User decides to edit a product - Change must reflect on batch card, user must first create a
		self.selenium.find_element_by_id('addQuality').click() 
		time.sleep(1) 
		self.selenium.find_element_by_id('InserBatch_heading').click()
		self.insert_Batch(
			'Batch',
			'Test R&D Project',
			'z4567 second_testNewProductType',
			201,
			6789
			)
		self.wait_for_(lambda: self.find_object_by_id("QualityObject_subject", "201201 - 123456789"))
		time.sleep(1)
		self.selenium.find_element_by_id('addQuality').click() 
		time.sleep(1) 
		self.selenium.find_element_by_id('editProductType_heading').click()
		time.sleep(1)
		self.selenium.find_element_by_id('searchProductTypeInput').send_keys("second")
		self.selenium.find_element_by_id('searchProductType_Submit').submit()
		self.wait_for_(lambda: self.find_object_by_id("productTypeSearchResult_description", "second_testNewProductType"))
		self.closeNotifications()
		time.sleep(5)
		self.selenium.find_element_by_id('editRDProject_Toggle').click() 
		self.edit_ProductType(
			"z5678",
			"edited_testNewProductType")

		# # refresh
		# self.alert_wait()
		# alertObj = self.selenium.switch_to.alert
		# alertObj.accept()

		time.sleep(5)
		self.wait_for_(lambda: self.find_object_by_id("QualityObject_product", "z5678 edited_testNewProductType"))

		# User decides to delete an product - All Batch Cards with corresponding product must get removed as well
		self.selenium.find_element_by_id('refreshQualityPlanList').click()
		self.closeNotifications()
		time.sleep(3)
		self.selenium.find_element_by_id('addQuality').click() 
		time.sleep(1) 
		self.selenium.find_element_by_id('editProductType_heading').click()
		time.sleep(1)
		self.selenium.find_element_by_id('searchProductTypeInput').clear()
		self.selenium.find_element_by_id('searchProductTypeInput').send_keys("edited")
		self.selenium.find_element_by_id('searchProductType_Submit').submit()
		time.sleep(1)
		self.closeNotifications()
		time.sleep(5)
		self.selenium.find_element_by_id('deleteBatchProduct_Toggle').click()
		self.selenium.find_element_by_xpath('//span[@ajaxStatus="deleteBatchProduct"]').click()

		# Information correct?
		self.alert_wait()
		alertObj = self.selenium.switch_to.alert
		alertObj.accept()

		# # refresh
		# self.alert_wait()
		# alertObj = self.selenium.switch_to.alert
		# alertObj.accept()
		# time.sleep(5)
		
		self.wait_for_(lambda: self.find_object_by_id("noDataQualityObject", "No data here!"))
		
		print("\nTEST: def test_1_editDelete_ProductType_RDPlan_BatchCard_All -> complete]\n")
		return False

