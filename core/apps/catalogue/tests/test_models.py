from django.contrib.auth.models import User
from django.test import TestCase

from core.apps.catalogue.models import Category, Product


class TestCategoriesModel(TestCase):
  def setUp(self):
    self.data1 = Category.objects.create(name='Programming', slug='Programming')

  def test_category_model_entry(self):
    data = self.data1
    self.assertTrue(isinstance(data, Category))

  def test_category_model_entry(self):
    data = self.data1
    self.assertEqual(str(data), 'Programming')

class TestProductsModel(TestCase):
  def setUp(self):
    Category.objects.create(name='Programming', slug='Programming')
    User.objects.create(username='Extra-admin')
    self.data1 = Product.objects.create(category_id=1, title='Grokking Algorithm', created_by_id=1, 
                                        slug='grokking-algorithm', price='34.99', image='Grokking')

  def test_product_model_entry(self):
    data = self.data1
    self.assertTrue(isinstance(data, Product))
    self.assertEqual(str(data), 'Grokking Algorithm')
