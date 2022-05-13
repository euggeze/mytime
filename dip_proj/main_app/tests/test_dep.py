"""Module for testing rest-modules"""
import json

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from django.test import TestCase, Client

from main_app.models import Department


class DepartmentTestCase(APITestCase):
    """Class for testing CRUD functions
    and unexpected situations for department view"""

    def setUp(self):
        self.client = Client()
        self.department = Department.objects.create(name="Test Department")

    def test_list(self):
        """Testing list departments"""
        response = self.client.get(reverse('department-list'))
        response_data = response.json()
        db_data = Department.objects.all()
        self.assertEqual(200, response.status_code)
        self.assertNotEqual(Department.objects.count(), 0)
        for i in range(len(db_data)):
            self.assertEqual(response_data[i].get('name'), db_data[i].name)



    def test_create(self):
        """Testing create a department"""
        past_count = Department.objects.count()
        response = self.client.post(reverse('department-list'), {'name': 'TEST'}, format='json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(past_count + 1, Department.objects.count())
        self.assertTrue(Department.objects.filter(name='TEST').exists())


    def test_create_empty(self):
        """Testing create a empty department"""
        past_count = Department.objects.count()
        response = self.client.post(reverse('department-list'), {'name': ''}, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(past_count, Department.objects.count())
        self.assertFalse(Department.objects.filter(name='').exists())


    def test_create_long(self):
        """Testing create long department name"""
        name = 'TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST T'
        past_count = Department.objects.count()
        response = self.client.post(reverse('department-list'), {'name': name}, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(past_count, Department.objects.count())
        self.assertFalse(Department.objects.filter(name=name).exists())

    def test_createa(self):
        """Testing create a department"""
        past_count = Department.objects.count()
        response = self.client.post(reverse('department-list'), {'name': 'TEST'}, format='json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(past_count + 1, Department.objects.count())
        self.assertTrue(Department.objects.filter(name='TEST').exists())

    def test_create_emptay(self):
        """Testing create a empty department"""
        past_count = Department.objects.count()
        response = self.client.post(reverse('department-list'), {'name': ''}, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(past_count, Department.objects.count())
        self.assertFalse(Department.objects.filter(name='').exists())

    def test_create_along(self):
        """Testing create long department name"""
        name = 'TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST T'
        past_count = Department.objects.count()
        response = self.client.post(reverse('department-list'), {'name': name}, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(past_count, Department.objects.count())
        self.assertFalse(Department.objects.filter(name=name).exists())

    def test_creaate(self):
        """Testing create a department"""
        past_count = Department.objects.count()
        response = self.client.post(reverse('department-list'), {'name': 'TEST'}, format='json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(past_count + 1, Department.objects.count())
        self.assertTrue(Department.objects.filter(name='TEST').exists())

    def test_creatae_empty(self):
        """Testing create a empty department"""
        past_count = Department.objects.count()
        response = self.client.post(reverse('department-list'), {'name': ''}, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(past_count, Department.objects.count())
        self.assertFalse(Department.objects.filter(name='').exists())

    def test_creatae_long(self):
        """Testing create long department name"""
        name = 'TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST T'
        past_count = Department.objects.count()
        response = self.client.post(reverse('department-list'), {'name': name}, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(past_count, Department.objects.count())
        self.assertFalse(Department.objects.filter(name=name).exists())

    def test_creaate(self):
        """Testing create a department"""
        past_count = Department.objects.count()
        response = self.client.post(reverse('department-list'), {'name': 'TEST'}, format='json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(past_count + 1, Department.objects.count())
        self.assertTrue(Department.objects.filter(name='TEST').exists())

    def test_create_emptay(self):
        """Testing create a empty department"""
        past_count = Department.objects.count()
        response = self.client.post(reverse('department-list'), {'name': ''}, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(past_count, Department.objects.count())
        self.assertFalse(Department.objects.filter(name='').exists())

    def test_create_lonag(self):
        """Testing create long department name"""
        name = 'TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST T'
        past_count = Department.objects.count()
        response = self.client.post(reverse('department-list'), {'name': name}, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(past_count, Department.objects.count())
        self.assertFalse(Department.objects.filter(name=name).exists())

    def test_creatae_lodng(self):
        """Testing create long department name"""
        name = 'TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST T'
        past_count = Department.objects.count()
        response = self.client.post(reverse('department-list'), {'name': name}, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(past_count, Department.objects.count())
        self.assertFalse(Department.objects.filter(name=name).exists())

    def test_creaatde(self):
        """Testing create a department"""
        past_count = Department.objects.count()
        response = self.client.post(reverse('department-list'), {'name': 'TEST'}, format='json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(past_count + 1, Department.objects.count())
        self.assertTrue(Department.objects.filter(name='TEST').exists())

    def test_create_empdtay(self):
        """Testing create a empty department"""
        past_count = Department.objects.count()
        response = self.client.post(reverse('department-list'), {'name': ''}, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(past_count, Department.objects.count())
        self.assertFalse(Department.objects.filter(name='').exists())

    def test_create_londag(self):
        """Testing create long department name"""
        name = 'TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST T'
        past_count = Department.objects.count()
        response = self.client.post(reverse('department-list'), {'name': name}, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(past_count, Department.objects.count())
        self.assertFalse(Department.objects.filter(name=name).exists())

    def test_creaastde(self):
        """Testing create a department"""
        past_count = Department.objects.count()
        response = self.client.post(reverse('department-list'), {'name': 'TEST'}, format='json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(past_count + 1, Department.objects.count())
        self.assertTrue(Department.objects.filter(name='TEST').exists())

    def test_create_empdstay(self):
        """Testing create a empty department"""
        past_count = Department.objects.count()
        response = self.client.post(reverse('department-list'), {'name': ''}, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(past_count, Department.objects.count())
        self.assertFalse(Department.objects.filter(name='').exists())

    def test_create_empdstcay(self):
        """Testing create a empty department"""
        past_count = Department.objects.count()
        response = self.client.post(reverse('department-list'), {'name': ''}, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(past_count, Department.objects.count())
        self.assertFalse(Department.objects.filter(name='').exists())

    def test_create_londsag(self):
        """Testing create long department name"""
        name = 'TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST T'
        past_count = Department.objects.count()
        response = self.client.post(reverse('department-list'), {'name': name}, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(past_count, Department.objects.count())
        self.assertFalse(Department.objects.filter(name=name).exists())