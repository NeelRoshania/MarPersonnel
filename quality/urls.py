"""marindec1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views
from quality.views import BaseView, RefreshQualityView, DeleteQualityView, EditPaintInfo, HandleQualityPagination, EditRDProjectView, EditBatchProductView

app_name = 'quality'

urlpatterns = [
    url(r'^qualityBaseView/?$', BaseView.as_view(), name='index'),
    url(r'^quality/update/?$', RefreshQualityView.as_view(), name='update_quality'),
    # url(r'^CustomerID/update/?$', RefreshCustomerIDView.as_view(), name='update_CustomerID'),
    # url(r'^deliveryplan/update/(?P<pk>[\w-]+)/$', EditDeliveryPlanView.as_view(), name='edit_DeliveryPlan'), 
    url(r'^qualityPlan/delete/(?P<pk>[\w-]+)/$', DeleteQualityView.as_view(), name='delete_QualityPlan'),
    url(r'^qualityPlan/edit/(?P<pk>[\w-]+)/$', EditPaintInfo.as_view(), name='edit_QualityPlan'),
    url(r'^handleQualityPagination/?$', HandleQualityPagination.as_view(), name='quality_handlePagination'),
    # url(r'^customerID/search_EDIT/?$', SearchCustomerIDView.as_view(), name='search_EDIT_CustomerID'), 
    url(r'^rdProject/delete/(?P<pk>[\w-]+)/$', DeleteQualityView.as_view(), name='delete_rdProject'), 
    url(r'^rdProject/edit/(?P<pk>[\w-]+)/$', EditRDProjectView.as_view(), name='editRDProject'),
    url(r'^batchProduct/delete/(?P<pk>[\w-]+)/$', DeleteQualityView.as_view(), name='delete_batchProduct'), 
    url(r'^batchProduct/edit/(?P<pk>[\w-]+)/$', EditBatchProductView.as_view(), name='editBatchProduct'),
    # # url(r'^customerID/searchDeliveryPlans/?$', SearchDeliveryPlanView.as_view(), name='searchDeliveryPlans'),
    ]
