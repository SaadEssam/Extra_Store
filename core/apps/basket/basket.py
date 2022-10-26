from decimal import Decimal

from core.apps.checkout.models import DeliveryOptions
from django.conf import settings
from core.apps.catalogue.models import Product


class Basket():
  # Base Basket Class
  def __init__(self, request):
    self.session = request.session
    basket = self.session.get(settings.BASKET_SESSION_ID)
    if settings.BASKET_SESSION_ID not in request.session:
      basket = self.session[settings.BASKET_SESSION_ID] = {}
    self.basket = basket

  def add(self, product, qty):
    # Adding & updating the basket
    product_id = str(product.id)
    if product_id in self.basket:
      self.basket[product_id]['qty'] = qty
    else:
      self.basket[product_id] = {'price': str(product.regular_price), 'qty': qty}
    self.save()

  def __iter__(self):
    # Collect product_id to query DB & return products
    product_ids = self.basket.keys()
    products = Product.objects.filter(id__in=product_ids)
    basket = self.basket.copy()

    for product in products:
      basket[str(product.id)]['product'] = product

    for item in basket.values():
      item['price'] = Decimal(item['price'])
      item['total_price'] = item['price'] * item['qty']
      yield item

  def __len__(self):
    # Count the qty of items

    return sum(item['qty'] for item in self.basket.values())

  def get_subtotal_price(self):
    return sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())

  def get_delivery_price(self):
    new_price = 0.00

    if "purchase" in self.session:
      new_price = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price
    
    return new_price

  def get_total_price(self):
    new_price = 0.00
    subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
    
    if "purchase" in self.session:
      new_price = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price
    total = subtotal + Decimal(new_price)
    return total

  def basket_update_delivery(self, delivery_price=0):
    subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())
    total = subtotal + Decimal(delivery_price)
    return total

  def delete(self, product):
    # Delete item from basket
    product_id = str(product)
    if product_id in self.basket:
      del self.basket[product_id]
    self.save()

  def update(self, product, qty):
    # Update item from basket
    product_id = str(product)
    if product_id in self.basket:
      self.basket[product_id]['qty'] = qty
    self.save()


  def clear(self):
    # Remove basket from session
    del self.session[settings.BASKET_SESSION_ID]
    del self.session["address"]
    del self.session["purchase"]
    self.save()

  def save(self):
    self.session.modified = True
