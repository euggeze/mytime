"""The `urlpatterns` list routes URLs to views for department_app"""
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from main_app.views import user_reg, user_login
from main_app.service import MainPageTemplate,ActivityPageTemplate, TaskDelete, TaskCreate, TaskEdit, TimesheetDelete, NotificationPageTemplate,VacationCreate,VacationInfo, VacationDec, SettingsPageTemplate

urlpatterns = [
    path('signup/', user_reg.signup, name='signup'),
    path('activate/<uidb64>/<token>/',
        user_reg.activate, name='activate'),
    path('login/', user_login.userlogin, name='login'),
    path('logout/', user_login.userlogout, name='logout'),
    path('', user_login.open_mainpage, name='mainpage'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password-reset/change_password.html',
             subject_template_name='password-reset/password_reset_subject.txt',
             email_template_name='password-reset/password_reset_email.html',
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='change_pass.html',
            success_url = '/'
        ),
        name='change_password'
    ),
    path('<int:pk>/', MainPageTemplate.as_view(template_name='main_page.html'), name='mainpage_list_start'),
    path('<int:pk>/activities/', ActivityPageTemplate.as_view(template_name='project_activities.html'), name='activities_page'),
path('<int:pk>/activities/undefined/', user_login.without_undef, name='without_undef'),
    path('delete_task/<int:pk>/', TaskDelete.as_view(), name='task_delete'),
path('delete_timesheet/<int:pk>/', TimesheetDelete.as_view(), name='delete_timesheet'),
path('task_create/<int:pk>/', TaskCreate.as_view(), name='task_create'),
path('timesheet_edit/<int:pk>/', TaskEdit.as_view(template_name='create_activity.html'), name='task_edit'),
path('<int:pk>/vacation/', NotificationPageTemplate.as_view(template_name='notifications.html'), name='notification_page'),
path('<int:pk>/newrequest/', VacationCreate.as_view(template_name='create_request_vac.html'), name='newrequest'),
path('inforequest/<int:pk>/', VacationInfo.as_view(template_name='request_detail.html'), name='vacation_info'),
path('createanswer/<int:pk>/', VacationDec.as_view(template_name='WFA_request.html'), name='vacation_answer'),
path('<int:pk>/settings/', SettingsPageTemplate.as_view(template_name='settings.html'), name='settings'),
path('accounts/', include('allauth.urls')),
]