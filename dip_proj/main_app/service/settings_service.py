"""Module for working with a main page in site"""
import requests
import datetime
import pandas
import json

from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.list import MultipleObjectMixin
from rest_framework.reverse import reverse

from main_app.models import Task, Employee, Timesheet

user = None

class SettingsPageTemplate(UpdateView):
    """ Template for view the list activities"""
    model = Employee
    fields = '__all__'
    object = None

    def get_success_url(self):
        """ Function for save page for delete success"""
        return reverse('settings', args=[user])

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        global user
        user = request.user.pk
        if request.user.pk != self.kwargs['pk']:
            return HttpResponseRedirect(reverse('mainpage_list_start', args=[request.user.pk]))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """ Function for get data from api"""
        global user
        employee = requests.get(reverse('employee-detail', request=self.request, args=[user])).json()
        user_data = requests.get(reverse('user-detail', request=self.request, args=[user])).json()
        data = super().get_context_data(**kwargs)
        employee['name'] = employee['first_name'] + " " + employee['last_name'][0] + "."
        data['data_employee'] = employee
        data['today_is'] = str(datetime.datetime.now().strftime("%B")) + ", " + str(datetime.date.today().day)
        data['pk'] = user
        data['user_data'] = user_data
        print(data['user_data'])
        return data

    def get(self, request, *args, **kwargs):
        global user
        context = self.get_context_data(**kwargs)
        context["qs_json"] = Employee.objects.filter(manager=user).values()
        context['list_emp'] = requests.get(reverse("employee-list", request=self.request) + "?manager=" + str(user)).json()
        for x in range(len(context["qs_json"])):
            context["qs_json"][x]['name'] = " " + context["qs_json"][x]["first_name"] + " " + context["qs_json"][x]["last_name"]
            context["qs_json"][x]["photo"] = context['list_emp'][x]["photo"]
        context["qs_json"] = json.dumps(list(context["qs_json"]))
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        """ Function get for update vacations"""

        success_url = self.get_success_url()
        empl_change = Employee.objects.get(user=self.kwargs["pk"])
        user_change = User.objects.get(id=self.kwargs["pk"])
        if request.FILES.get("myfile",None) and request.POST.get("submit_photo", None):
            empl_change.photo = request.FILES.get("myfile",None)
            empl_change.save()
        elif request.POST.get("submit_personal", None):
            empl_change.first_name = request.POST.get("first_name",None)
            empl_change.last_name = request.POST.get("last_name",None)
            user_change.username = request.POST.get("email",None)
            empl_change.save()
            user_change.save()
        return HttpResponseRedirect(success_url)