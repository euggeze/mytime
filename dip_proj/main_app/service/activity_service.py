"""Module for working with a main page in site"""
import requests
import datetime
import pandas
import json
import xlsxwriter

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.list import MultipleObjectMixin
from rest_framework.reverse import reverse
from io import BytesIO

from main_app.models import Task, Employee, Timesheet

user = None


def WriteToExcel(data):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("Timesheet")
    title = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'center',
        'valign': 'vcenter'
    })
    title_table = workbook.add_format({
        'bold': True,
        'align': 'center',
        'valign': 'vcenter'
    })
    header = workbook.add_format({
        'color': 'black',
        'align': 'center',
        'valign': 'top'
    })
    table = workbook.add_format({
        'color': 'black',
        'align': 'center',
        'valign': 'top',
        'border': 1
    })
    title_text = f"Employee worksheet: {data['data_employee']['first_name']} {data['data_employee']['last_name']}"
    worksheet_s.merge_range('B2:H2', title_text, title)
    worksheet_s.write(4, 0, ugettext("Department"), header)
    worksheet_s.write(4, 1, ugettext(data['data_employee']['department']), header)
    worksheet_s.write(5, 0, ugettext("Status"), header)
    worksheet_s.write(5, 1, ugettext(data['data_employee']['status']), header)
    worksheet_s.write(6, 0, ugettext("Date from"), header)
    worksheet_s.write(6, 1, ugettext(data['first_day']), header)
    worksheet_s.write(7, 0, ugettext("Date to"), header)
    worksheet_s.write(7, 1, ugettext(data['last_day']), header)
    worksheet_s.set_column('A:A', 25)
    worksheet_s.set_column('B:B', 15)
    worksheet_s.write(10, 0, "Activities", table)
    for x in range(len(data['days'])):
        worksheet_s.write(10, x+1,data['days_d'][x],table)
    a = 11
    for x in range(len(data["data_activities"])):
        worksheet_s.write(a, 0, data['data_activities'][x]["project"], title_table)
        a+=1
        for y in range(len(data["data_activities"][x]["tasks"])):
            worksheet_s.write(a, 0, data['data_activities'][x]["tasks"][y]["task"], table)
            for z in range(len(data["data_activities"][x]["tasks"][y]["data"])):
                worksheet_s.write(a, z+1, data['data_activities'][x]["tasks"][y]["data"][z], table)
            a+=1
    worksheet_s.write(a, 0, "Non project activities", title_table)
    a+=1
    worksheet_s.write(a, 0, "Sick leave", table)
    for x in range(len(data["sick_leave"])):
        worksheet_s.write(a, x + 1, data["sick_leave"][x], table)
    a += 1
    worksheet_s.write(a, 0, "Paid leave", table)
    for x in range(len(data["paid_leave"])):
        worksheet_s.write(a, x + 1, data["paid_leave"][x], table)
    a += 1
    worksheet_s.write(a, 0, "Unpaid leave", table)
    for x in range(len(data["unpaid_leave"])):
        worksheet_s.write(a, x + 1, data["unpaid_leave"][x], table)
    a += 1
    worksheet_s.write(a, 0, "Day off", table)
    for x in range(len(data["day_off"])):
        worksheet_s.write(a, x + 1, data["day_off"][x], table)
    a += 1
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data

class ActivityPageTemplate(ListView):
    """ Template for view the list activities"""
    model = Task
    fields = '__all__'
    object_list = None


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        global user
        user = request.user.pk
        manager = requests.get(reverse('employee-detail', request=self.request, args=[self.kwargs['pk']])).json()["manager"]
        if request.user.pk != self.kwargs['pk'] and request.user.pk != manager:
            return HttpResponseRedirect(reverse('mainpage_list_start', args=[request.user.pk]))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """ Function for get data from api"""
        global user
        employee = requests.get(reverse('employee-detail', request=self.request, args=[user])).json()
        data = MultipleObjectMixin.get_context_data(self, **kwargs)
        employee['name'] = employee['first_name'] + " " + employee['last_name'][0] + "."
        data['data_employee'] = employee
        employee = requests.get(reverse('employee-detail', request=self.request, args=[self.kwargs['pk']])).json()
        data['data_empl'] = employee
        data['data_empl']['department'] = requests.get(reverse('department-detail', request=self.request,
                                                              args=[data['data_empl']['department']])).json()["name"]
        data['data_empl']['status'] = requests.get(reverse('department-detail', request=self.request,
                             args=[data['data_empl']['status']])).json()["name"]
        data['data_empl']['level'] = requests.get(reverse('department-detail', request=self.request,
                             args=[data['data_empl']['level']])).json()["name"]
        data['today_is'] = str(datetime.datetime.now().strftime("%B")) + ", " + str(datetime.date.today().day)
        data['pk'] = self.kwargs["pk"]
        return data

    def get(self, request, *args, **kwargs):
        global user
        days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        context = self.get_context_data(**kwargs)
        weekday = datetime.datetime.today().weekday()
        start = request.GET.get("start", "")
        finish = request.GET.get("end", "")
        excel = request.GET.get("excel", None)
        if start == "":
            start = str(datetime.date.today() - datetime.timedelta(weekday))
        else:
            new_start = start.split("/")
            start = "-".join([new_start[2],new_start[1],new_start[0],])
        if finish == "":
            if weekday<5:
                finish = str(datetime.date.today() + datetime.timedelta(4 - weekday))
            else:
                finish = str(datetime.date.today() + datetime.timedelta(6 - weekday))
        else:
            new_finish = finish.split("/")
            finish = "-".join([new_finish[2],new_finish[1],new_finish[0],])
        filter_query = '?start=' + start + '&finish=' + finish + '&pk=' + str(self.kwargs['pk'])
        activities = requests.get(reverse('timesheet-list', request=self.request) + filter_query).json()
        weekdates = pandas.date_range(start=start, end=finish)
        weekdates_int = [x.day for x in weekdates]
        weekdays = [days[x.weekday()] for x in weekdates]
        days = [weekdays[i]+", "+str(weekdates_int[i]) for i in range(len(weekdays))]
        context.setdefault('days_d', days)
        try:
            days[weekdates.get_loc((str(datetime.date.today())))] += " TDY"
        except:
            print('without today')
        context.setdefault('days', days)
        context.setdefault('first_day', start)
        context.setdefault('last_day', finish)
        project_list = requests.get(reverse('projectlist-list', request=self.request) + '?pk=' + str(self.kwargs['pk'])).json()
        data = set()
        for x in range(len(activities)):
            data.add(activities[x]["task"])
        actions = []
        for x in range(len(activities)):
                activities[x]["task_date"] = weekdates.get_loc(activities[x]["task_date"])
        for x in range(len(project_list)):
            actions.append({})
            actions[x].setdefault("project",project_list[x]["project"])
            actions[x].setdefault("project_id", project_list[x]["project"])
        for x in range(len(project_list)):
            actions[x].setdefault("tasks", [])
            all_tasks = []
            for y in data:
                for z in range(len(activities)):
                    if activities[z]["project"] == actions[x]["project"] and y == activities[z]["task"]:
                        if y not in all_tasks:
                            actions[x]["tasks"].append({})
                            actions[x]["tasks"][-1].setdefault("task",y)
                            actions[x]["tasks"][-1].setdefault("task_id", y)
                            actions[x]["tasks"][-1].setdefault("data", ["-" for x in range(len(weekdates))])
                        all_tasks = [actions[x]["tasks"][o]["task"] for o in range(len(actions[x]["tasks"]))]
        unpaid_leave = ["-" for x in range(len(weekdates))]
        day_off = ["-" for x in range(len(weekdates))]
        paid_leave = ["-" for x in range(len(weekdates))]
        sick_leave = ["-" for x in range(len(weekdates))]
        proj = requests.get(reverse('project-list', request=self.request) + "?proj=EPAM").json()[0]["id"]
        for z in range(len(activities)):
            if activities[z]["project"] == proj:
                if activities[z]["task"] == requests.get(reverse('task-list', request=self.request)+"?task=Unpaid leave").json()[0]["id"]:
                    unpaid_leave[activities[z]["task_date"]] = activities[z]["task_time"]
                elif activities[z]["task"] == requests.get(reverse('task-list', request=self.request)+"?task=Day off").json()[0]["id"]:
                    day_off[activities[z]["task_date"]] = activities[z]["task_time"]
                elif activities[z]["task"] == requests.get(reverse('task-list', request=self.request)+"?task=Paid leave").json()[0]["id"]:
                    paid_leave[activities[z]["task_date"]] = activities[z]["task_time"]
                elif activities[z]["task"] == requests.get(reverse('task-list', request=self.request)+"?task=Sick leave").json()[0]["id"]:
                    sick_leave[activities[z]["task_date"]] = activities[z]["task_time"]
        context.setdefault('unpaid_leave', unpaid_leave)
        context.setdefault('day_off',day_off)
        context.setdefault('paid_leave',paid_leave)
        context.setdefault('sick_leave',sick_leave)
        for x in range(len(project_list)):
            for y in range(len(activities)):
                for z in range(len(actions[x]["tasks"])):
                    if actions[x]["tasks"][z]["task"] == activities[y]["task"] and activities[y]["task_time"]>0:
                        actions[x]["tasks"][z]["data"][activities[y]["task_date"]] = activities[y]["task_time"]
        for x in range(len(project_list)):
            actions[x]["project"] = requests.get(reverse('project-detail', request=self.request,
                                                              args=[project_list[x]["project"]])).json()["project_name"]
            for z in range(len(actions[x]["tasks"])):
                actions[x]["tasks"][z]["task"] = requests.get(reverse('task-detail', request=self.request,
                                                              args=[actions[x]["tasks"][z]["task"]])).json()["task_name"]
        context.setdefault('data_activities', actions)
        context.setdefault('project_list', project_list)
        context.setdefault('width', str(len(weekdays)*100)+"px")
        context["qs_json"] = Employee.objects.filter(manager=user).values()
        context['list_emp'] = requests.get(reverse("employee-list", request=self.request) + "?manager=" + str(user)).json()
        for x in range(len(context["qs_json"])):
            context["qs_json"][x]['name'] = " " + context["qs_json"][x]["first_name"] + " " + context["qs_json"][x]["last_name"]
            context["qs_json"][x]["photo"] = context['list_emp'][x]["photo"]
        context["qs_json"] = json.dumps(list(context["qs_json"]))
        if excel:
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
            context["data_employee"]["department"] = requests.get(reverse('department-detail', request=self.request,
                                                              args=[context["data_employee"]["department"]])).json()["name"]
            context["data_employee"]["status"] = requests.get(reverse('status-detail', request=self.request,
                                                                          args=[context["data_employee"][
                                                                                    "status"]])).json()["name"]
            xlsx_data = WriteToExcel(context)
            response.write(xlsx_data)
            return response
        print(context["data_activities"])
        return self.render_to_response(context)

class TaskDelete(DeleteView):
    """ Template for view delete employee"""
    model = Task
    fields = '__all__'

    def get_success_url(self):
        """ Function for save page for delete success"""
        return reverse('activities_page', args=[user])

    def post(self, request, *args, **kwargs):
        """ Function get for delete department"""
        success_url = self.get_success_url()
        id_task = kwargs['pk']
        requests.delete(reverse('task-detail', request=self.request, args=[id_task]))
        return HttpResponseRedirect(success_url)

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

class TaskCreate(CreateView):
    """ Template for view delete employee"""
    model = Task
    fields = '__all__'

    def get_success_url(self):
        """ Function for save page for delete success"""
        return reverse('activities_page', args=[user])

    def post(self, request, *args, **kwargs):
        """ Function get for delete department"""
        success_url = self.get_success_url()
        id_proj = kwargs['pk']
        defxt = "New activity"
        task = {"task_name": defxt}
        requests.post(reverse('task-list', request=self.request), data=task)
        tasks_dict = requests.get(reverse('task-list', request=self.request)).json()
        id_task = None
        for x in tasks_dict:
            if x["task_name"] == "New activity":
                id_task = x["id"]
        timesheet = {"task_time": 0,
        "task_date": str(datetime.date.today()),
        "project": id_proj,
        "employee": user,
        "task": id_task}
        requests.post(reverse('timesheet-list', request=self.request), data=timesheet)
        return HttpResponseRedirect(success_url)

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

class TaskEdit(UpdateView):
    """ Template for view delete employee"""
    model = Task
    fields = '__all__'
    object = None

    def get_success_url(self):
        """ Function for save page for delete success"""
        return reverse('activities_page', args=[user])

    def get_context_data(self, **kwargs):
        global user
        employee = requests.get(reverse('employee-detail', request=self.request, args=[user])).json()
        print(employee)
        data = super().get_context_data(**kwargs)
        employee['name'] = employee['first_name'] + " " + employee['last_name'][0] + "."
        data['data_employee'] = employee
        data['pk'] = user
        task = requests.get(reverse('task-detail', request=self.request, args=[self.kwargs['pk']])).json()
        data['task']= task
        data['date']= str(datetime.date.today())
        return data

    def post(self, request, *args, **kwargs):
        """ Function get for delete department"""
        success_url = self.get_success_url()
        context = self.get_context_data(**kwargs)
        task = request.POST.get("task_name",None)
        date_task = request.POST.get("date_task", None)
        time_task = request.POST.get("time_task", None)
        filter_query = '?task=' + str(self.kwargs['pk'])
        proj = requests.get(reverse('timesheet-list', request=self.request) + filter_query).json()[0]["project"]
        if task != context["task"]["task_name"]:
            requests.put(reverse('task-detail', request=self.request, args=[self.kwargs['pk']]),data={"task_name":task})
        timesheet = {"task_time": time_task,
                     "task_date": date_task,
                     "project": proj,
                     "employee": user,
                     "task": self.kwargs['pk']}
        tasks = requests.get(reverse('timesheet-list', request=self.request) + filter_query).json()
        for x in tasks:
            if x["task_date"]==timesheet["task_date"]:
                requests.put(reverse('timesheet-detail',request=self.request, args=[x["id"]]),data=timesheet)
                print(x)
                return HttpResponseRedirect(success_url)
        requests.post(reverse('timesheet-list', request=self.request), data=timesheet)
        return HttpResponseRedirect(success_url)
