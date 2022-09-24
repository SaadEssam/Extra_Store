


class Basket():
  
  def __init__(self, request):
    self.session = request.session
    basket = self.session.get('s-key')
    if 's-key' not in request.session:
      basket = self.session['s-key'] = {}
    self.basket = basket
    
    
  def add(self, product):
    
    product_id = product.id
    if product_id not in self.basket:
      self.basket[product_id] = {'price': str(product.price)}
      
    self.session.modified = True
