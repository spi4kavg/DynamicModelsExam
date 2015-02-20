from django.test import TestCase
from django.core.urlresolvers import reverse
from django.db.models import get_model
import datetime


class ExamPageTest(TestCase):

	def setUp(self):
		self.url = reverse('dynamic_models', args=['users'])
		self.not_exist = reverse('dynamic_models', args=['asd'])

	def test_get(self):
		"""
			check allowed methods
		"""
		response = self.client.get(self.url, {})
		self.assertEqual(response.status_code, 200)

	def test_not_exists_model_get(self):
		"""
			check not exists model
		"""
		response = self.client.get(self.not_exist, {})
		self.assertEqual(response.status_code, 404)

	def test_post(self):
		"""
			check we can add row into table
		"""
		response = self.client.post(self.url, {
			"date_joined": datetime.date.today(),
			"name": "user_test",
			"paycheck": 100
		})
		self.assertEqual(response.status_code, 200)

	def test_error_post(self):
		"""
			check not exists model
		"""
		response = self.client.get(self.not_exist, {})
		self.assertEqual(response.status_code, 404)

	def test_not_allowed_methods(self):
		"""
			check not allowed methods
		"""
		response_put = self.client.put(self.url, {})
		response_delete = self.client.delete(self.url, {})

		self.assertEqual(response_put.status_code, 405)
		self.assertEqual(response_delete.status_code, 405)


class ExamEditTest(TestCase):

	def setUp(self):
		try:
			self.model = get_model('test_app', 'users')
			inst = self.model(
				date_joined=datetime.date.today(),
				name='user_test',
				paycheck=100
			)
			inst.save()
			self.pk = inst.id
		except LookupError:
			print('test is failed')
		self.url = reverse('dynamic_models_edit', args=['users', self.pk])

	def test_allowed_methods(self):
		"""
			check allowed methods
		"""
		response = self.client.post(self.url, {
			"id": self.pk,
			"paycheck": 200
		})
		self.assertEqual(response.status_code, 200)
		paycheck = self.model.objects.get(id=self.pk).paycheck
		self.assertEqual(200, paycheck)

	def test_not_allowed_methods(self):
		"""
			check not allowed methods
		"""
		response_put = self.client.put(self.url, {})
		response_delete = self.client.delete(self.url, {})
		response_get = self.client.get(self.url, {})

		self.assertEqual(response_put.status_code, 405)
		self.assertEqual(response_delete.status_code, 405)
		self.assertEqual(response_get.status_code, 405)