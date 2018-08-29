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
from production.models import RMReference
import time


# StaticLiveServerTestCase -> serve static files during test, spin up development server for test, creates and deletes test database without interfering with production database
class TestSearchObject(FunctionalTest):
	# Generic search for a Production Meeting

	def test_1_search_ProductionMeeting_All(self):

		print("\ndef:test_1_search_ProductionMeeting_All -> complete\n")

