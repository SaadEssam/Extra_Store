from django.shortcuts import render
# Create your views here.

def basket_summary(request):
  return render(request, 'store/basket/summary.html')