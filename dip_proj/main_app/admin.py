from django.contrib import admin

# Register your models here.

from .models import Employee, Department, Level, Project, ProjectList, Status, StatusVacation, Task, Timesheet, TypeVacation, Vacation, PhotoModel

admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Level)
admin.site.register(Project)
admin.site.register(ProjectList)
admin.site.register(Status)
admin.site.register(StatusVacation)
admin.site.register(Task)
admin.site.register(Timesheet)
admin.site.register(TypeVacation)
admin.site.register(Vacation)
admin.site.register(PhotoModel)

