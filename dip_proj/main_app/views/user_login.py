from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.reverse import reverse
from allauth.socialaccount.forms import DisconnectForm
from allauth.socialaccount import signals


from main_app.forms import LoginForm


def userlogin(request):
    if request.user.is_authenticated:
       return HttpResponseRedirect(reverse('mainpage_list_start', args=[request.user.pk]))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('mainpage_list_start', args=[user.pk]))
                else:
                    return HttpResponse('Disabled account')
            else:
                return render(request, 'login_with_error.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def without_undef(request):
    if request.user.is_authenticated:
       return HttpResponseRedirect(reverse('mainpage_list_start', args=[request.user.pk]))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('mainpage_list_start', args=[user.pk]))
                else:
                    return HttpResponse('Disabled account')
            else:
                return render(request, 'login_with_error.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def open_mainpage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('mainpage_list_start', args=[request.user.pk]))
    return HttpResponseRedirect('login')


