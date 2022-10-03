from django.shortcuts import render, redirect
from .forms import RegistrationForm

# Create your views here.

def account_register(request):

  if request.user.is_authenticated:
    return redirect('/')

  if request.method == 'POST':
    registerForm = RegistrationForm(request.POST)
    if registerForm.is_valid():
      user = registerForm.save(commit=False)
      user.email = registerForm.cleaned_data('email')
      user.set_password(registerForm.cleaned_data['password'])
      user.is_active = False
      user.save()
