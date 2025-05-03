"""
URL configuration for crm_application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from crmapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home, name="home"),
    path('register/', Register, name="register"),

    path('login/', Login, name="login"),

    path('logout/',Logout, name="logout"),
    
    path('dashboard/',Dashboard, name="dashboard"),
    
    path('customer_list/',Customer_list, name="customer_list"),
    
    path('create_customer/',Create_customer, name="create_customer"),
    
    path('lead_list/',Lead_list, name="lead_list"),
    
    path('create_lead/',Create_lead, name="create_lead"),
    
    path('view_customer/<int:id>/', View_customer, name='view_customer'),
    
    path('view_lead/<int:id>/', View_lead, name='view_lead'),
    
    path('customer/update/<int:id>/', Update_customer, name='update_customer'),
    
    path('lead/update/<int:id>/', Update_lead, name='update_lead'),
    
    path('customer/delete/<int:id>/', Delete_customer, name='delete_customer'),
    
    path('lead/delete/<int:id>/', Delete_lead, name='delete_lead'),
    
    path('convert-lead/<int:id>/', Convert_lead_to_customer, name='convert_lead_to_customer'),
    
    path('lead_report/',Lead_report, name="lead_report"),
    
    path('customer_report/',Customer_report, name="customer_report"),
    
    path('create_email_group/', Create_Email_group, name='create_email_group'),
    
    path('email_group_list/', Email_group_list, name='email_group_list'),
    
    path('email_group/view/<int:group_id>/', View_email_group, name='view_email_group'),
    
    path('email/letterhead/', Letterhead, name='letterhead'),
    
    path('email-history/', Email_history, name='email_history'),
 
]
