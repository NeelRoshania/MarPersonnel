
from django.conf.urls import url, include
from django.contrib import admin
from . import views
from production.views import BaseView, RefreshProductionView, DeleteModelView, EditProductionMeetingView, EditProductionNoteView, EditRMShortageView, EditMaintenanceIssueView, EditProductionPlanView, HandleProductionPagination, EditRMReference

app_name = 'production'

urlpatterns = [
        url(r'^productionBaseView/?$', BaseView.as_view(), name='index'),
        url(r'^updateProduction/?$', RefreshProductionView.as_view(), name='update_productionList'),
        url(r'^prodMeeting/delete/(?P<pk>[\w-]+)/$', DeleteModelView.as_view(), name='delete_productionMeeting'),
        url(r'^prodMeeting/edit/(?P<pk>[\w-]+)/$', EditProductionMeetingView.as_view(), name='edit_ProductionMeeting'),
        url(r'^prodNote/delete/(?P<pk>[\w-]+)/$', DeleteModelView.as_view(), name='delete_productionNote'),
        url(r'^prodMeetingNote/edit/(?P<pk>[\w-]+)/$', EditProductionNoteView.as_view(), name='edit_ProductionNote'),
        url(r'^RawMaterial/edit/(?P<pk>[\w-]+)/$', EditRMReference.as_view(), name='edit_RawMaterial'),
        url(r'^RawMaterial/delete/(?P<pk>[\w-]+)/$', DeleteModelView.as_view(), name='delete_RMShortage'),
        url(r'^RMShortage/edit/(?P<pk>[\w-]+)/$', EditRMShortageView.as_view(), name='edit_RMShortage'),
        url(r'^RMShortage/delete/(?P<pk>[\w-]+)/$', DeleteModelView.as_view(), name='delete_RMShortage'),
        url(r'^MaintenanceIssue/edit/(?P<pk>[\w-]+)/$', EditMaintenanceIssueView.as_view(), name='edit_MaintenanceIssue'),
        url(r'^MaintenanceIssue/delete/(?P<pk>[\w-]+)/$', DeleteModelView.as_view(), name='delete_MaintenanceIssue'),
        url(r'^ProductionPlan/edit/(?P<pk>[\w-]+)/$', EditProductionPlanView.as_view(), name='edit_ProductionPlan'),
        url(r'^ProductionPlan/delete/(?P<pk>[\w-]+)/$', DeleteModelView.as_view(), name='delete_ProductionPlan'),
        url(r'^searchProduction/?$', HandleProductionPagination.as_view(), name='search_productionPagination'),
    ]

EditRMReference