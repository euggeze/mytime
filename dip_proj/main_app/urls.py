"""The `urlpatterns` list routes URLs to views for department_app"""
from django.urls import path
from rest_framework.routers import SimpleRouter
from django.contrib.auth import views as auth_views

from main_app.views import employee_view, department_view, level_view, project_view, projectlist_view, status_view, \
    statusvacation_view, task_view, timesheet_view, typevacation_view, vacation_view, user_view, user_reg, user_login, blockcolor_view

router = SimpleRouter()
router.register("employee", employee_view.EmployeeViewSet, basename='employee')
router.register("department", department_view.DepartmentViewSet, basename='department')
router.register("level", level_view.LevelViewSet, basename='level')
router.register("project", project_view.ProjectViewSet, basename='project')
router.register("projectlist", projectlist_view.ProjectListViewSet, basename='projectlist')
router.register("status", status_view.StatusViewSet, basename='status')
router.register("statusvacation", statusvacation_view.StatusVacationViewSet, basename='statusvacation')
router.register("task", task_view.TaskViewSet, basename='task')
router.register("timesheet", timesheet_view.TimesheetViewSet, basename='timesheet')
router.register("typevacation", typevacation_view.TypeVacationViewSet, basename='typevacation')
router.register("vacation", vacation_view.VacationViewSet, basename='vacation')
router.register("user", user_view.UserViewSet, basename='user')
router.register("block_color", blockcolor_view.BlockColorViewSet, basename='block_color')

urlpatterns = router.urls
