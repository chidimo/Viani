from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import Group

from model_mommy import mommy

from personnel.models import Person, Personnel


class TestCustomerModel(TestCase):
    def setUp(self):
        self.customer = mommy.make('shop.Customer')

    def test_model_representation(self):
        """Test model representation and get_absolute_url"""
        self.assertEqual(
            self.customer.__str__(),
            f'{self.customer.first_name.title()}, {self.customer.last_name.title()}'
        )
        self.assertEqual(
            self.customer.get_absolute_url(), reverse('shop:customer_index')
        )

class JobModel(TestCase):
    def setUp(self):
        self.job = mommy.make('shop.Job')

    def test_model_representation(self):
        """Test model representation"""
        self.assertEqual(
            self.job.__str__(),
            f'{self.job.description.title()}'
        )
        self.assertEqual(
            self.job.get_absolute_url(), reverse('shop:job_index')
        )