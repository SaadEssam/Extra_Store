import stripe

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
  
  print('total')
  
  stripe.api_key = 'sk_test_51LpvHqJsaKztgHd5Uspc2tJQ1EcUkhGkO7pOnM8RcWiwVRdHBDFAVk6CdT02DROAg463IDV5AR8OrDZDn5SEIPi8003nAdFP67'
  intent = stripe.PaymentIntent.create(
    amount=total,
    currency='usd',
    metadata={'userid': request.user.id}
  )
  
  return render(request, 'payment/home.html', {'client_secret': intent.client_secret})
