# TO run this test -> python manage.py test unit_tests.tests.test_ajaxified_views

# List of assertion methods for py TestCase -> https://docs.python.org/3/library/unittest.html#assert-methods

from .base import UnitTest
from django.core.urlresolvers import reverse_lazy

# Define subclass of test case to instantiate a unit test
class ViewsTests(UnitTest):

	# Test to see if index url reverses correctly and generates template, home.html
	def test_renders_homepage_template(self):
		response = self.client.get(reverse_lazy('home:index'))
		self.assertTemplateUsed(response, 'home/home.html')
		print("TEST: test_renders_homepage_template -> Pass")

	# Test to see if refresh url reverses correctly and generates template, objectList.html -> to return object data 
	def test_renders_refresh_template(self):
		response = self.client.get(reverse_lazy('home:update_objectList'))
		self.assertTemplateUsed(response, 'home/includes/objectList.html')
		print("TEST: test_renders_refresh_template -> Pass")

	# Test to see if search url reverses correctly and generates template, objectList.html -> to return object data
	def test_renders_search_template(self):
		response = self.client.get(reverse_lazy('home:search_object'))
		self.assertTemplateUsed(response, 'home/includes/objectList.html')
		print("TEST: test_renders_search_template -> Pass")