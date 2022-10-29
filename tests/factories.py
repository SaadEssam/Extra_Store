import factory
from core.apps.catalogue.models import (
  Category, 
  Product, 
  ProductType, 
  ProductSpecification, 
  ProductSpecificationValue,)
from core.apps.account.models import Address, Customer
from faker import Faker


fake = Faker()

####
# Catalogue
####

class CategoryFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Category
  
  name = "programming"
  slug = "programming"


class ProductTypeFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = ProductType
    django_get_or_create = ("name",)
  
  name = "book"


class ProductSpecificationFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = ProductSpecification
  
  product_type = factory.SubFactory(ProductTypeFactory)
  name = "Pages"


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
      model = Product

    product_type = factory.SubFactory(ProductTypeFactory)
    category = factory.SubFactory(CategoryFactory)
    title = "product_title"
    description = fake.text()
    slug = "product_slug"
    regular_price = "35.99"
    discount_price = "30.99"


class ProductSpecificationValueFactory(factory.django.DjangoModelFactory):
    class Meta:
      model = ProductSpecificationValue

    product = factory.SubFactory(ProductFactory)
    specification = factory.SubFactory(ProductSpecificationFactory)
    value = "100"


####
# Account
####

class CustomerFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Customer
  
  email = "t@t.com"
  name = "admin"
  mobile = '0105659885'
  password = 'password'
  is_active = True
  is_staff = False

  @classmethod
  def _create(cls, model_class, *args, **kwargs):
    manager = cls._get_manager(model_class)
    if "is_superuser" in kwargs:
      return manager.create_superuser(*args, **kwargs)
    else:
      return manager.create_user(*args, **kwargs)


class AddressFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Address
  
  Customer = factory.SubFactory(CustomerFactory)
  full_name = fake.name()
  phone = fake.phone_number()
  postcode = fake.postcode()
  address_line = fake.street_address()
  address_line2 = fake.street_address()
  town_city = fake.city_suffix()