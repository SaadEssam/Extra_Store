from store.models import Product
from decimal import Decimal


class Basket():
  # Base Basket Class
  
  def __init__(self, request):
    self.session = request.session
    basket = self.session.get('skey')
    if 'skey' not in request.session:
      basket = self.session['skey'] = {}
    self.basket = basket
    
    
  def add(self, product, qty):
    # Adding & updating the basket
    
    product_id = product.id
    if product_id not in self.basket:
      self.basket[product_id] = {'price': str(product.price), 'qty':int(qty)}
      
    self.session.modified = True

  def __iter__(self):
    # Collect product_id to query DB & return products
    
    product_ids = self.basket.keys()
    products = Product.products.filter(id__in=product_ids)
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
