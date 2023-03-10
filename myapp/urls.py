"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),

    ##################### ADMIN ################################
    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_changepassword', views.admin_changepassword, name='admin_changepassword'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('admin_home', views.admin_home, name='admin_home'),

    path('admin_house_type_add', views.admin_house_type_add, name='admin_house_type_add'),
    path('admin_house_type_view', views.admin_house_type_view, name='admin_house_type_view'),
    path('admin_house_type_delete', views.admin_house_type_delete, name='admin_house_type_delete'),
    path('admin_house_type_edit', views.admin_house_type_edit, name='admin_house_type_edit'),

    path('admin_user_details_view', views.admin_user_details_view, name='admin_user_details_view'),
    path('admin_user_details_delete', views.admin_user_details_delete, name='admin_user_details_delete'),

    path('admin_owner_details_pending_view', views.admin_owner_details_pending_view, name='admin_owner_details_pending_view'),
    path('admin_owner_details_delete', views.admin_owner_details_delete, name='admin_owner_details_delete'),
    path('admin_owner_details_view', views.admin_owner_details_view, name='admin_owner_details_view'),
    path('admin_owner_details_register_update', views.admin_owner_details_register_update, name='admin_owner_details_register_update'),

    path('admin_house_details_pending_view', views.admin_house_details_pending_view, name='admin_house_details_pending_view'),
    path('admin_house_details_register_update', views.admin_house_details_register_update, name='admin_house_details_register_update'),

    path('owner_house_pic_add', views.owner_house_pic_add, name='owner_house_pic_add'),
    path('owner_house_pic_delete', views.owner_house_pic_delete, name='owner_house_pic_delete'),
    path('owner_house_pic_view', views.owner_house_pic_view, name='owner_house_pic_view'),

    ##################################### OWNER ##############################
    path('owner_login', views.owner_login_check, name='owner_login'),
    path('owner_logout', views.owner_logout, name='owner_logout'),
    path('owner_home', views.owner_home, name='owner_home'),
    path('owner_details_add', views.owner_details_add, name='owner_details_add'),
    path('owner_changepassword', views.owner_changepassword, name='owner_changepassword'),
    path('owner_profile_view', views.owner_profile_view, name='owner_profile_view'),

    path('owner_house_details_add', views.owner_house_details_add, name='owner_house_details_add'),
    path('owner_house_details_view', views.owner_house_details_view, name='owner_house_details_view'),
    path('owner_house_details_delete', views.owner_house_details_delete, name='owner_house_details_delete'),
    path('owner_house_details_edit', views.owner_house_details_edit, name='owner_house_details_edit'),
    path('owner_house_details_pending_view', views.owner_house_details_pending_view, name='owner_house_details_pending_view'),

    ##################### USER #########################################
    path('user_login', views.user_login_check, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('user_home', views.user_home, name='user_home'),
    path('user_details_add', views.user_details_add, name='user_details_add'),
    path('user_changepassword', views.user_changepassword, name='user_changepassword'),

]
