from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from basket.basket import Basket
# Create your views here.

@login_required
def BasketView(request):
  
  basket = Basket(request)
  total = str(basket.get_total_price())
  total = total.replace('.', '')
  total = int(total)
  
  stripe.api.key = 'pk_test_51LpvHqJsaKztgHd5j9lnHRRlRrcMAW33Hlaost9eZD1ckuXGiiz5ptmN4FPR10fo8I5nCNf7rUHHN6N140qRbor300eT2kbrGS'
  intent = stripe.PaymentIntent.create(
    amount=total,
    currency='usd',
    metadata={'userid': request.user.id}
  )
  
  return render(request, 'payment/home.html', {'client_secret': intent.client_secret})