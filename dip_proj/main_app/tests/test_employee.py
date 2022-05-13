"""Module for testing Employee view"""
import json

from django.contrib.auth.models import User
from django.test import TestCase, Client

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from main_app.models import Employee, Department, Level, Status


class EmployeeTestCase(APITestCase):
    """Class for testing CRUD functions
    and unexpected situations for employee view"""

    def setUp(self):
        self.client = Client()
        self.expected_keys = {key.name for key in Employee._meta.fields}
        self.department = Department.objects.create(name="Test Department")
        self.level = Level.objects.create(name="Test level")
        self.status = Status.objects.create(name="Test status")
        self.user = User.objects.create(password="test", first_name='test', last_name='test', email='test@test.test', username="test")
        self.employee = Employee.objects.create(user=self.user , first_name="Employee", last_name="test",
                                                department=self.department, status=self.status, level=self.level)


    def test_list(self):
        """Testing list Employee model"""
        response = self.client.get(reverse('employee-list'))
        self.assertEqual(200, response.status_code)
        self.assertNotEqual(Employee.objects.count(), 0)

    def test_list_department_employee(self):
        """Testing list Employee model with filter"""
        response = self.client.get(reverse('employee-list')+'?department=Testing')
        response_data = response.json()
        db_data = Employee.objects.filter(department=Department.objects.get(name='Test Department'))
        self.assertEqual(200, response.status_code)
        self.assertNotEqual(Employee.objects.count(), 0)









