from account.models import Address
from basket.basket import Basket
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render

from .models import DeliveryOptions

# Create your views here.

@login_required
def delivery_choices(request):
  delivery_options = DeliveryOptions.objects.filter(is_active=True)
  return render(request, "checkout/delivery_choices.html", {"delivery_options": delivery_options})

@login_required
def basket_update_delivery(request):
  basket = Basket(request)
  if request.POST.get("action") == "post":
    delivery_option = int(request.POST.get("delivery_option"))
    delivery_type = DeliveryOptions.objects.get(id=delivery_option)
    updated_total_price = basket.basket_update_delivery(delivery_type.delivery_price)
    
    session = request.session
    if "purchase" not in request.session:
      session["purchase"] = {
        "delivery_id": delivery_type.id,
      }
    else:
      session["purchase"]["delivery_id"] = delivery_type.id
      session.modified = True
    
    response = JsonResponse({"total": updated_total_price, "delivery_price": delivery_type.delivery_price})
    return response

@login_required
def delivery_address(request):
  session = request.session
  if "purchase" not in request.session:
    messages.success(request, "Please select delivery option")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])
  
  addresses = Address.objects.filter(customer=request.user).order_by("-default")
  
  if "address" not in request.session:
    session["address"] = {"address_id": str(addresses[0].id)}
  else:
    session["address"]["address_id"] = str(addresses[0].id)
    session.modified = True
    
  return render(request, "checkout/delivery_address.html", {"addresses": addresses})

@login_required
def payment_selection(request):
  
  session = request.session
  if "address" not in request.session:
    messages.success(request, "Please select address option")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])
  return render(request, "checkout/payment_selection.html", {})

@login_required
def payment_complete(request):
  PPClinet = PayPalClient()
  
  body = json.loads(request.body)
  data = body["orderID"]
  user_id = request.user.id
  
