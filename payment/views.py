import stripe
import json

from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from basket.basket import Basket
from orders.views import payment_confirmation
# Create your views here.

@login_required
def BasketView(request):
  
  basket = Basket(request)
  total = str(basket.get_total_price())
  total = total.replace('.', '')
  
  
  stripe.api_key = 'sk_test_51LpvHqJsaKztgHd5Uspc2tJQ1EcUkhGkO7pOnM8RcWiwVRdHBDFAVk6CdT02DROAg463IDV5AR8OrDZDn5SEIPi8003nAdFP67'
  intent = stripe.PaymentIntent.create(
    amount=total,
    currency='usd',
    metadata={'userid': request.user.id}
  )
  
  return render(request, 'payment/home.html', {'client_secret': intent.client_secret})


@csrf_exempt
def stripe_webhook(request):
  payload = request.body
  event = None
  print('12312312')

  try:
    event = stripe.Event.construct_from(
      json.loads(payload), stripe.api_key
    )
  except ValueError as e:
    print(e)
    return HttpResponse(status=400)
  
  if event.type == 'payment_intent.succeeded':
    payment_confirmation(event.data.object.client_secret)
    
  else:
    print('Unhandled event type {}'.format(event.type))

  return HttpResponse(status=200)

def order_placed(request):
  basket = Basket(request)
  basket.clear()
  return render(request, 'payment/orderplaced.html')