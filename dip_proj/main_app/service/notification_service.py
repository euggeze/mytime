"""Module for working with a notification page in site"""
import requests
import datetime
import pandas
import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.http import urlsafe_base64_encode
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.list import MultipleObjectMixin
from rest_framework.reverse import reverse

from main_app.models import Vacation, Employee, Timesheet, TypeVacation, StatusVacation


user = None

class NotificationPageTemplate(ListView):
    """ Template for view the list activities"""
    model = Vacation
    fields = '__all__'
    object_list = None

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
        data = MultipleObjectMixin.get_context_data(self, **kwargs)
        employee['name'] = employee['first_name'] + " " + employee['last_name'][0] + "."
        data['data_employee'] = employee
        data['today_is'] = str(datetime.datetime.now().strftime("%B")) + ", " + str(datetime.date.today().day)
        data['pk'] = user
        return data

    def get(self, request, *args, **kwargs):
        global user
        context = self.get_context_data(**kwargs)
        app = "Approved"
        dd = 'Denied'
        approve = requests.get(reverse('statusvacation-list', request=self.request) + "?status_vac=" + app).json()
        denied = requests.get(reverse('statusvacation-list', request=self.request) + "?status_vac=" + dd).json()
        context["requests"] = requests.get(reverse("vacation-list", request=self.request)+"?employee="+ str(user)).json()
        for x in context["requests"]:
            x["str_in_list"] = f'Your vacation from {x["start_date"]} to {x["finish_date"]} has '
            if x["status_vacation"] == approve[0]["id"]:
                x.setdefault("img_v","fa fa-check fa-3x")
                x["str_in_list"] += 'been approved'
            elif x["status_vacation"] == denied[0]["id"]:
                x.setdefault("img_v", "fa fa-times fa-4x")
                x["str_in_list"] += 'been denied'
            else:
                x.setdefault("img_v", "fa fa-question fa-5x")
                x["str_in_list"] += 'not been approved yet'
            x["status_vacation"] = \
            requests.get(reverse('statusvacation-detail', request=self.request, args=[x["status_vacation"]])).json()[
                "status_vacation"]

        context['list_emp'] = requests.get(reverse("employee-list", request=self.request) + "?manager=" + str(user)).json()
        strwfa = "Wait for approval"
        WFA = requests.get(reverse('statusvacation-list', request=self.request)+"?status_vac="+strwfa).json()
        context["requests_manager"] = []
        for x in context['list_emp']:
            empl = requests.get(reverse("vacation-list", request=self.request) + "?employee=" + str(x["user"])).json()
            employee_name = requests.get(reverse('employee-detail', request=self.request, args=[x["user"]])).json()
            for y in empl:
                if y["status_vacation"] == WFA[0]["id"]:
                    context["requests_manager"].append(y)
                    context["requests_manager"][-1].setdefault("name", employee_name["first_name"]+" "+employee_name["last_name"])
        context["qs_json"] = Employee.objects.filter(manager=user).values()
        for x in range(len(context["qs_json"])):
            context["qs_json"][x]['name'] = " " + context["qs_json"][x]["first_name"] + " " + context["qs_json"][x]["last_name"]
            context["qs_json"][x]["photo"] = context['list_emp'][x]["photo"]
        context["qs_json"] = json.dumps(list(context["qs_json"]))
        return self.render_to_response(context)

class VacationCreate(CreateView):
    model = Vacation
    fields = '__all__'
    object = None

    def get_success_url(self):
        """ Function for save page for delete success"""
        return reverse('notification_page', args=[user])

    def get_context_data(self, **kwargs):
        global user
        employee = requests.get(reverse('employee-detail', request=self.request, args=[user])).json()
        data = super().get_context_data(**kwargs)
        employee['name'] = employee['first_name'] + " " + employee['last_name'][0] + "."
        data['data_employee'] = employee
        data['pk'] = user
        data['date'] = str(datetime.date.today())
        data['vac_types'] = requests.get(reverse('typevacation-list', request=self.request)).json()
        return data

    def post(self, request, *args, **kwargs):
        """ Function get for delete department"""

        success_url = self.get_success_url()
        strwfa = "Wait for approval"
        WFA = requests.get(reverse('statusvacation-list', request=self.request) + "?status_vac=" + strwfa).json()

        new_vac = Vacation(start_date= request.POST.get('date_start',None),
                           finish_date= request.POST.get('date_finish', None),
        photo_approve= request.FILES.get('myfile', None),
        comment_emp= request.POST.get('comment', None),
    employee= get_object_or_404(Employee, user=user),
        type_vacation= get_object_or_404(TypeVacation, id=request.POST.get('id_select', None)),
        status_vacation= get_object_or_404(StatusVacation, id=WFA[0]["id"])
        )
        new_vac.save()
        return HttpResponseRedirect(success_url)

class VacationInfo(ListView):
    model = Vacation
    fields = '__all__'
    object_list = None

    def get_context_data(self, **kwargs):
        global user
        employee = requests.get(reverse('employee-detail', request=self.request, args=[user])).json()
        data = super().get_context_data(**kwargs)
        employee['name'] = employee['first_name'] + " " + employee['last_name'][0] + "."
        data['data_employee'] = employee
        data['pk'] = user
        data['date'] = str(datetime.date.today())
        data['vac_types'] = requests.get(reverse('typevacation-list', request=self.request)).json()
        return data

    def get(self, request, *args, **kwargs):
        global user
        context = self.get_context_data(**kwargs)
        vacation = requests.get(reverse('vacation-detail', request=self.request,args=[self.kwargs["pk"]])).json()
        if vacation["employee"]==user:
            context["vacation"] = vacation
            context["vacation"]["type_vacation"] = requests.get(reverse('typevacation-detail', request=self.request,
                                                                        args=[context["vacation"]["type_vacation"]])).json()["type_vacation"]
            context["vacation"]["status_vacation"] = requests.get(reverse('statusvacation-detail', request=self.request,
                                                                        args=[context["vacation"]["status_vacation"]])).json()[
                "status_vacation"]
            context["vacation"]["employee"] = requests.get(reverse('employee-detail', request=self.request,
                                                                        args=[user])).json()["first_name"] + " " +\
            requests.get(reverse('employee-detail', request=self.request,
                                 args=[user])).json()["last_name"]
            return self.render_to_response(context)
        return HttpResponseRedirect(reverse('notification_page', args=[user]))

class VacationDec(UpdateView):
    model = Vacation
    fields = '__all__'
    object = None

    def get_success_url(self):
        """ Function for save page for delete success"""
        return reverse('notification_page', args=[user])

    def get_context_data(self, **kwargs):
        global user
        employee = requests.get(reverse('employee-detail', request=self.request, args=[user])).json()
        data = super().get_context_data(**kwargs)
        employee['name'] = employee['first_name'] + " " + employee['last_name'][0] + "."
        data['data_employee'] = employee
        data['pk'] = user
        data['date'] = str(datetime.date.today())
        data['vac_types'] = requests.get(reverse('typevacation-list', request=self.request)).json()
        return data

    def get(self, request, *args, **kwargs):
        global user
        context = self.get_context_data(**kwargs)
        vacation = requests.get(reverse('vacation-detail', request=self.request,args=[self.kwargs["pk"]])).json()
        employee = requests.get(reverse('employee-detail', request=self.request, args=[vacation["employee"]])).json()
        if employee["manager"]==user:
            context["vacation"] = vacation
            context["vacation"]["type_vacation"] = requests.get(reverse('typevacation-detail', request=self.request,
                                                                        args=[context["vacation"]["type_vacation"]])).json()["type_vacation"]
            context["vacation"]["status_vacation"] = requests.get(reverse('statusvacation-detail', request=self.request,
                                                                        args=[context["vacation"]["status_vacation"]])).json()[
                "status_vacation"]
            context["vacation"]["employee"] = requests.get(reverse('employee-detail', request=self.request,
                                                                        args=[vacation["employee"]])).json()["first_name"] + " " +\
            requests.get(reverse('employee-detail', request=self.request,
                                 args=[vacation["employee"]])).json()["last_name"]
            context["vac_status"]=requests.get(reverse('statusvacation-list', request=self.request)).json()
            print(vacation)
            return self.render_to_response(context)
        return HttpResponseRedirect(reverse('notification_page', args=[user]))

    def post(self, request, *args, **kwargs):
        """ Function get for update vacations"""

        success_url = self.get_success_url()
        new_vac = Vacation.objects.get(id=self.kwargs["pk"])
        new_vac.comment = request.POST.get('comment', None)
        new_vac.status_vacation = get_object_or_404(StatusVacation, id=request.POST.get('id_select', None))
        new_vac.save()
        vacation = requests.get(reverse('vacation-detail', request=self.request, args=[self.kwargs["pk"]])).json()
        t_vac = requests.get(reverse('task-list', request=self.request)+"?task="+request.POST.get('vac_type', None)).json()[0]["id"]
        proj = requests.get(reverse('project-list', request=self.request)+"?proj=EPAM").json()[0]["id"]
        date_start = request.POST.get('date_start', None)
        date_finish = request.POST.get('date_finish', None)
        if requests.get(reverse('statusvacation-detail', request=self.request,args=[request.POST.get('id_select', None)])).json()["status_vacation"] == "Approved":
            date_mas = pandas.date_range(date_start,date_finish,freq='d')
            for x in date_mas:
                timesheet = {"task_time": 8,
                             "task_date": str(x.to_pydatetime().date()),
                             "project": proj,
                             "employee": vacation["employee"],
                             "task": t_vac}
                print(timesheet)
                requests.post(reverse('timesheet-list', request=self.request), data=timesheet)
        return HttpResponseRedirect(success_url)
