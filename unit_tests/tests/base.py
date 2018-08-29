# TO run this test -> python manage.py test unit_tests.tests.test_ajaxified_models

# Unit tests,
# 	- Change or add test below to manage implementation of expected behaviour,
# 		- Expected behaviour tested through functional/end-end tests
		# - If funcitonal test fails, use unit tests to manage implementation i.e. back end processes to allow functional test to pass

from django.test import TestCase
from django.core.urlresolvers import reverse_lazy, reverse
from datetime import datetime, date
import time

# Base class for ModelTests and ViewTests
class UnitTest(TestCase):

	# This methods can be used to make a HTTP GET or POST request with a number of arguments
	# 	- It was primarily designed to allow unit tests to pass valid and invalid form field values
	# 	- The advantages are,
	# 		- any number of arguments can be passed
	# 		- any number of form fields and values can be passed as defined by ModelForm
	# 		- Valid and invalid form data can be passed depending on above
	# 	- The key to understanding how posting and getting views is to understand what is required from the view in question under views.py
	# 	- Description,
	# 		- post_data => Data to be passed to server
	# 		- args => url arguments
	# 		- url => url to post/get information
	# 		- post => if True, will make a post request
	# 		- ajaxConditionals => boolean dictionary as part of design structure of mixins.py
	# 		- form => to be defined
	# 		- object => to be defined
	# 	- Improvements include,
	# 		- Desgning error handling classes for try except statements

	def get_httpResponse(self, url, post, object=None, post_data=None, form=None, args=None, ajaxConditionals=None):
		# If get=True then post
		if post:
			if args and not ajaxConditionals:
				try:
					_ = self.client.post(reverse(url, args=args), HTTP_X_REQUESTED_WITH='XMLHttpRequest')	
					return _
				except:
					return self.fail("PostRequestError: Unknown url.")

			# This conditional is triggering because both states ar true
			if (post_data and ajaxConditionals and not args):
				data = {**post_data, **ajaxConditionals}	# Combine both dictionaries into one
				try:
					print('{}{}{}{}'.format("UnitTestBase Type 1 Data to pass: ", data, " to -> ", reverse_lazy(url)))
					_ = self.client.post(reverse_lazy(url), data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')	
					return _
				except:
					return self.fail("PostRequestError: post_data error or unknown url.")

			# If only posting data, url args and ajaxConditionals
			elif (post_data and ajaxConditionals and args):
				try:
					_ = {**post_data, **ajaxConditionals}
					print('{}{}'.format("UnitTestBase Type 2 Data to pass: ", _))
					_ = self.client.post(reverse(url, args=args), data=_, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
					return _
				except:
					return self.fail("PostRequestError: form error, unknown url, missing args or incorrect ajaxConditionals.")
			# If only posting data, url args and ajaxConditionals
			elif (ajaxConditionals and args):
				try:
					_ = {**ajaxConditionals}
					print('{}{}'.format("UnitTestBase Type 3 Data to pass: ", _))
					_ = self.client.post(reverse(url, args=args), data=_, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
					return _
				except:
					return self.fail("PostRequestError: Unknown url, invalid/missing args or incorrect ajaxConditionals.")

			else:
				return self.fail("PostRequestError: Methods requires either form instance and args, or post_data and ajaxConditionals.")			
		else:
			# If url arguments exist
			if args:
				try:
					_ = self.client.get(
					reverse(url, args=(args)),
					HTTP_X_REQUESTED_WITH='XMLHttpRequest'
					)
					return _
				except:
					return self.fail("GetRequestError: Argument error or unknown url.")
			# If no other arguments
			elif post_data:
					# searchObjectFieldText
					data = {**post_data, **ajaxConditionals}
					print('{}{}'.format("Data to pass: ", data))
					try:
						return self.client.get(reverse_lazy(url), data=post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest',)
					except:
						return self.fail("GetRequestError: post_data error or unknown url.")
			else:
				try:
					_ = self.client.get(
					reverse_lazy(url),
					HTTP_X_REQUESTED_WITH='XMLHttpRequest',
					)
					return _
				except:
					return self.fail("GetRequestError: Unknown url.")