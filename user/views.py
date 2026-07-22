from django.shortcuts import render, redirect
from django.urls import reverse
from .form import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as dj_login, logout as dj_logout
from django.contrib.auth import authenticate
import logging

logger = logging.getLogger(__name__)

AUTH_BACKEND = 'django.contrib.auth.backends.ModelBackend'


@csrf_exempt
def signUp(request):
    if request.method == 'GET':
        return render(request, 'signUp.html', {'form': SignUpForm()})

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                dj_login(request, user, backend=AUTH_BACKEND)
                return redirect(reverse('home'))
            except Exception:
                logger.exception('Signup failed')
                return render(request, 'signUp.html', {
                    'form': form,
                    'errors': {'__all__': ['Could not create account. Please try again.']},
                })
        return render(request, 'signUp.html', {'form': form, 'errors': form.errors})

    return redirect(reverse('signup'))


@csrf_exempt
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'form': LoginForm()})

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username.lower(), password=password)
            if user:
                dj_login(request, user, backend=AUTH_BACKEND)
                return redirect(reverse('home'))
            return render(request, 'login.html', {
                'form': form,
                'error': 'Invalid username or password',
            })
        return render(request, 'login.html', {
            'form': form,
            'error': 'Invalid credentials',
        })

    return redirect(reverse('login'))


@csrf_exempt
def logout(request):
    dj_logout(request)
    return redirect(reverse('login'))
