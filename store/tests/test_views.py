from importlib import import_module
from unittest import skip

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, TestCase
from django.urls import reverse

from store.models import Category, Product
from store.views import all_products


@skip('demonstrating skipping')
class TestSkip(TestCase):
  def test_skip_ex(self):
    pass

class TestViewResponses(TestCase):
  def setUp(self):
    self.c = Client()
    User.objects.create(username='Extra-admin')
    Category.objects.create(name='Programming', slug='Programming')
    self.data1 = Product.objects.create(category_id=1, title='Grokking Algorithm', created_by_id=1, 
                                        slug='grokking-algorithm', price='34.99', image='Grokking')

  def test_url_allowed_hosts(self):
    """
    Test allowed hosts
    """
    response = self.c.get('/', HTTP_HOST='nodomain.com')
    self.assertEqual(response.status_code, 400)
    response = self.c.get('/', HTTP_HOST='yourdomain.com')
    self.assertEqual(response.status_code, 200)

  def test_product_detail_url(self):
    """
    Test Product status
    """
    response = self.c.get(reverse('store:product_detail', args=['grokking-algorithm']))
    self.assertEqual(response.status_code, 200)  

  def test_category_detail_url(self):
    """
    Test Category status
    """
    response = self.c.get(reverse('store:category_list', args=['Programming']))
    self.assertEqual(response.status_code, 200)

  def test_homepage_html(self):
    request = HttpRequest()
    engine = import_module(settings.SESSION_ENGINE)
    request.session = engine.SessionStore()
    response = all_products(request)
    html = response.content.decode('utf8')
    self.assertIn('<title>Extra Store</title>', html)
    self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
    self.assertTrue(response.status_code, 200)
