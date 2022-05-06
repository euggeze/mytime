"""Module for working with a main page in site"""
import random

import requests
import datetime
import json

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DeleteView
from django.views.generic.list import MultipleObjectMixin
from rest_framework.reverse import reverse

from main_app.models import Employee, Timesheet

user = None

class MainPageTemplate(ListView):
    """ Template for view the list department"""
    model = Employee
    fields = '__all__'

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
        working_week_time = 40
        working_time = 0
        employee = requests.get(reverse('employee-detail', request=self.request, args=[user])).json()
        data = MultipleObjectMixin.get_context_data(self, **kwargs)
        employee['name'] = employee['first_name']+" "+employee['last_name'][0]+"."
        data['data_employee'] = employee
        data['today_is'] = str(datetime.datetime.now().strftime("%B")) + ", " + str(datetime.date.today().day)
        data['pk'] = user
        weekday = datetime.datetime.today().weekday()
        start = str(datetime.date.today() - datetime.timedelta(weekday))
        finish = str(datetime.date.today() + datetime.timedelta(7 - weekday))
        filter_query = '?start=' + start + '&finish=' + finish + '&pk=' + str(user)
        activities = requests.get(reverse('timesheet-list', request=self.request) + filter_query).json()
        project_list = requests.get(reverse('projectlist-list', request=self.request) + '?pk=' + str(user)).json()
        block_colors = requests.get(reverse('block_color-list', request=self.request)).json()
        data['total_activities'] = len(activities)
        data['project_list'] = len(project_list)
        d = random.sample(range(0, 10), 10)
        actions = []
        a = 0
        for x in range(len(activities)):
                if activities[x]["task_time"] > 0:
                    working_time += activities[x]["task_time"]
                    actions.append({})
                    actions[-1].setdefault("act_id", activities[x]["id"])
                    actions[-1].setdefault("project", activities[x]["project"])
                    actions[-1].setdefault("project_id", activities[x]["project"])
                    actions[-1].setdefault("task", activities[x]["task"])
                    actions[-1].setdefault("task_id", activities[x]["task"])
                    actions[-1].setdefault("task_date", activities[x]["task_date"])
                    actions[-1].setdefault("task_time", str(activities[x]["task_time"])+" hours" )
                    actions[-1].setdefault("bg_color", block_colors[d[a]]["background_color"])
                    actions[-1].setdefault("progress_color", block_colors[d[a]]["progress_color"])
                    actions[-1].setdefault("progress", activities[x]["task_time"]/working_week_time*100)
                    a+=1
                    if a>9:
                        a=0

        for x in range(len(actions)):
            actions[x]["project"] = requests.get(reverse('project-detail', request=self.request,
                                                              args=[actions[x]["project_id"]])).json()["project_name"]
            actions[x]["task"] = requests.get(reverse('task-detail', request=self.request,
                                                              args=[actions[x]["task_id"]])).json()["task_name"]
        data['total_activities'] = len(actions)
        data['actions'] = actions
        data['not_worked'] = {"time": str(working_week_time-working_time)+" hours",
                              "progress": (working_week_time-working_time)/working_week_time*100,
                              "bg_color":block_colors[d[a]]["background_color"],
                              "progress_color":block_colors[d[a]]["progress_color"],
                              "number": working_week_time-working_time
                              }
        data["qs_json"] = Employee.objects.filter(manager=user).values()
        data['list_emp'] = requests.get(reverse("employee-list", request=self.request)+"?manager="+str(user)).json()
        for x in range(len(data["qs_json"])):

            data["qs_json"][x]['name'] = " " + data["qs_json"][x]["first_name"]+ " " + data["qs_json"][x]["last_name"]
            data["qs_json"][x]["photo"] = data['list_emp'][x]["photo"]
            data["qs_json"][x]["link"] = "{% url 'activities_page' pk=" +str(data['list_emp'][x]['user'])+" %}"
        data["qs_json"] = json.dumps(list(data["qs_json"]))

        app = "Approved"
        dd = 'Denied'
        approve = requests.get(reverse('statusvacation-list', request=self.request) + "?status_vac=" + app).json()
        denied = requests.get(reverse('statusvacation-list', request=self.request) + "?status_vac=" + dd).json()
        data["requests"] = requests.get(
            reverse("vacation-list", request=self.request) + "?employee=" + str(user)).json()
        for x in data["requests"]:
            x["str_in_list"] = f'Your vacation from {x["start_date"]} to {x["finish_date"]} has '
            if x["status_vacation"] == approve[0]["id"]:
                x.setdefault("img_v", "fa fa-check fa-3x")
                x["str_in_list"] += 'been approved'
            elif x["status_vacation"] == denied[0]["id"]:
                x.setdefault("img_v", "fa fa-times fa-4x")
                x["str_in_list"] += 'been denied'
            else:
                x.setdefault("img_v", "fa fa-question fa-5x")
                x["str_in_list"] += 'not been approved yet'
            x["status_vacation"] = \
                requests.get(
                    reverse('statusvacation-detail', request=self.request, args=[x["status_vacation"]])).json()[
                    "status_vacation"]

        data['list_emp'] = requests.get(
            reverse("employee-list", request=self.request) + "?manager=" + str(user)).json()
        strwfa = "Wait for approval"
        WFA = requests.get(reverse('statusvacation-list', request=self.request) + "?status_vac=" + strwfa).json()
        data["requests_manager"] = []
        for x in data['list_emp']:
            empl = requests.get(reverse("vacation-list", request=self.request) + "?employee=" + str(x["user"])).json()
            employee_name = requests.get(reverse('employee-detail', request=self.request, args=[x["user"]])).json()
            for y in empl:
                if y["status_vacation"] == WFA[0]["id"]:
                    data["requests_manager"].append(y)
                    data["requests_manager"][-1].setdefault("name",
                                                               employee_name["first_name"] + " " + employee_name[
                                                                   "last_name"])
        return data


class TimesheetDelete(DeleteView):
    """ Template for view delete employee"""
    model = Timesheet
    fields = '__all__'

    def get_success_url(self):
        """ Function for save page for delete success"""
        return reverse('mainpage_list_start', args=[user])

    def post(self, request, *args, **kwargs):
        """ Function get for delete department"""
        success_url = self.get_success_url()
        id_ts = kwargs['pk']
        requests.delete(reverse('timesheet-detail', request=self.request, args=[id_ts]))
        return HttpResponseRedirect(success_url)

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
