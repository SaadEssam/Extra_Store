from unittest import skip
from django.test import TestCase, Client, RequestFactory
from django.http import HttpRequest
from django.contrib.auth.models import User
from store.models import Category, Product
from django.urls import reverse
from store.views import all_products

class TestViewResponses(TestCase):
  def setUp(self):
    self.c = Client()
    self.factory = RequestFactory()
    User.objects.create(username='Extra-admin')
    Category.objects.create(name='Programming', slug='Programming')
    self.data1 = Product.objects.create(category_id=1, title='Grokking Algorithm', created_by_id=1, 
                                        slug='grokking-algorithm', price='34.99', image='Grokking')
    
  def test_url_allowed_hosts(self):
    """
    Test allowed hosts
    """
    response = self.c.get('/')
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
    response = all_products(request)
    html = response.content.decode('utf8')
    print(html)
    self.assertIn('<title>Home</title>', html)
    self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
    self.assertTrue(response.status_code, 200)
    
    
  def test_view_function(self):
    request = self.factory.get('/item/grokking-algorithms')
    response = all_products(request)
    html = response.content.decode('utf8')
    print(html)
    self.assertIn('<title>Home</title>', html)
    self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
    self.assertTrue(response.status_code, 200)