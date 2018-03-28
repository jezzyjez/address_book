from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^register$', views.registration, name='register'),
    re_path(r'^address$', views.address, name='address'),
    re_path(r'^add_contact$', views.add_contact, name='add_contact'),
    re_path(r'^export_contact$', views.export_contact, name='export_contact'),
    re_path(r'^upload_contact$', views.upload_contact, name='upload_contact'),
    re_path(r'^edit_contact/(?P<pk>\d+)$', views.edit_contact, name='edit_contact'),
    re_path(r'^delete_contact/(?P<pk>\d+)$', views.delete_contact, name='delete_contact'),
    ]
