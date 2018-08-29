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
from sales.views import BaseView, RefreshDeliveryPlanView, EditDeliveryPlanView, DeleteSalesView, SearchCustomerIDView, EditCustomerIDView, RefreshCustomerIDView, HandleSalesPagination

app_name = 'sales'

urlpatterns = [
    url(r'^salesBaseView/?$', BaseView.as_view(), name='index'),
    url(r'^deliveryplan/update/?$', RefreshDeliveryPlanView.as_view(), name='update_deliveryPlan'),
    url(r'^CustomerID/update/?$', RefreshCustomerIDView.as_view(), name='update_CustomerID'),
    url(r'^deliveryplan/update/(?P<pk>[\w-]+)/$', EditDeliveryPlanView.as_view(), name='edit_DeliveryPlan'), 
    url(r'^deliveryplan/delete/(?P<pk>[\w-]+)/$', DeleteSalesView.as_view(), name='delivered_deliveryPlan'),
    url(r'^handleSalesPagination/?$', HandleSalesPagination.as_view(), name='deliveryPlan_handlePagination'),
    url(r'^customerID/search_EDIT/?$', SearchCustomerIDView.as_view(), name='search_EDIT_CustomerID'), 
    url(r'^customerID/delete/(?P<pk>[\w-]+)/$', DeleteSalesView.as_view(), name='delete_customerID'), 
    url(r'^customerID/edit/(?P<pk>[\w-]+)/$', EditCustomerIDView.as_view(), name='editCustomerID'),
    # url(r'^customerID/searchDeliveryPlans/?$', SearchDeliveryPlanView.as_view(), name='searchDeliveryPlans'),
    ]
