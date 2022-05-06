import requests

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from main_app.forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from main_app.tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from rest_framework.reverse import reverse


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            print(request.POST)
            user = form.save(commit=False)
            user.is_active = False
            user.username = user.email
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            photo = requests.get(reverse('employee-detail', request=request, args=[1])).json()["photo"]
            employee = {'user': user.pk,
                        'first_name': request.POST.get('first_name', None),
                        'last_name': request.POST.get('last_name', None),
                        'position': 'Employee',
                        'department': 1,
                        'status': 1,
                        'level': 1,
                        "photo":photo}
            requests.post(reverse('employee-list', request=request), data=employee)
            return render(request, 'confirm_email_start.html', {'form': form})
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        #department = {'first_name': request.POST.get('first_name', None)}
        #requests.post(reverse('employee-list', request=request), data=department)
        # return redirect('home')
        return render(request, 'confirm_email_finish.html')
    else:
        return HttpResponse('Activation link is invalid!')