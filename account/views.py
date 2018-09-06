from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from account.forms import SignUpForm, QForm, AForm
from account.models import User, Question


def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {'unread_count': request.user.notifications.unread().count(),
                                                   'notifications': request.user.notifications.all()
                                                   })
    else:
        return render(request, 'home.html')


def editor(request):
    if request.method == 'POST':
        uf = QForm(request.POST)
        if uf.is_valid():
            uf.save()
            return HttpResponseRedirect(reverse('account:home'))
        else:
            print()
    else:
        form = QForm()
        return render(request, 'editortest.html', {'form': form,
                                                   'unread_count': request.user.notifications.unread().count(),
                                                   'notifications': request.user.notifications.all()
                                                   })


def answer(request):
    if request.method == 'POST':
        uf = AForm(request.POST)
        if uf.is_valid():
            answer_f = uf.save(commit=False)
            answer_f.responder = request.user
            answer_f.question = Question.objects.get(id=1)
            answer_f.save()
            return HttpResponseRedirect(reverse('account:home'))
        else:
            print()
    else:
        form = AForm()
        return render(request, 'answer.html', {'form': form,
                                                   'unread_count': request.user.notifications.unread().count(),
                                                   'notifications': request.user.notifications.all()
                                                   })


def signup(request):
    if request.method == 'POST':
        uf = SignUpForm(request.POST)
        if uf.is_valid():
            info = uf.instance
            user = User.objects.create_user(info.email, info.password, info.first_name, info.last_name)
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
