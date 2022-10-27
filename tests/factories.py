import factory
from core.apps.catalogue.models import (Category, Product, ProductType, ProductSpecification, ProductSpecificationValue)
from faker import Faker


fake = Faker()

# Catalogue

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
