


class Basket():
  
  def __init__(self, request):
    self.session = request.session
    basket = self.session.get('s-key')
    if 's-key' not in request.session:
      basket = self.session['s-key'] = {'number':4654565}
    self.basket = basket