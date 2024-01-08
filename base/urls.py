from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('',views.homePage,name='home'),
    path('ClientRequest',views.ClientRequestFunc,name='request'),
    path('status',views.Status,name='status'),
    path('report',views.report,name='report'),
    path('login',views.LoginPage,name='login'),
    path('register',views.RegisterPage,name='register'),
    path('admin_page',views.admin_page,name='admin_page'),
    path('allocate-request/', views.allot_request, name='allocate_request'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('reports/',views.reports , name='reports'),
    path('submit-report/<int:request_id>',views.submit_report , name='submit_report'),
    path('abc',views.abc , name='abc'),
    path('report-details/<int:report_id>/', views.report_details, name='report_details'),
    path('update-report/<int:report_id>/', views.update_report, name='update_report'),
    path('confirm-report/<int:report_id>/', views.confirm_report, name='confirm_report'),
    path('contact-us/', views.contact_us, name='contact_us'),
    # path('checkout/', views.create_checkout_session, name='create_checkout_session'),
    # path('success/', views.success, name='success'),
    # path('cancel/', views.cancel, name='cancel'),
    path('logout/', LogoutView.as_view(), name='logout')

]
