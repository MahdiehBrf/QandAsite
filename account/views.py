from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.urls import reverse

from account.forms import SignUpForm
from account.models import User


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        uf = SignUpForm(request.POST)
        if uf.is_valid():
            user = User.objects.create_user(uf.instance.email, uf.instance.password, uf.instance.first_name, uf.instance.last_name)
            user.save()
            return HttpResponseRedirect(reverse('account:home'))


def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('account:home'))