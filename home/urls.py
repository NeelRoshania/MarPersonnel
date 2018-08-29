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
from home.views import BaseView, RefershUserToDoView, DeleteModelView, EditUserToDoView, SearchUserToDoView, EditUserNoteView, EditNoteDescriptionView, HandleHomePagination

app_name = 'home'

urlpatterns = [
    url(r'^$', BaseView.as_view(), name='index'),
    url(r'^update/?$', RefershUserToDoView.as_view(), name='update_objectList'),
    url(r'^search/?$', SearchUserToDoView.as_view(), name='search_object'),
    url(r'^UserToDo/delete/(?P<pk>[\w-]+)/$', DeleteModelView.as_view(), name='delete_UserToDo'),
    url(r'^UserNote/delete/(?P<pk>[\w-]+)/$', DeleteModelView.as_view(), name='delete_UserNote'),
    url(r'^NoteDescription/delete/(?P<pk>[\w-]+)/$', DeleteModelView.as_view(), name='delete_NoteDescription'),
    url(r'^UserToDo/edit/(?P<pk>[\w-]+)/$', EditUserToDoView.as_view(), name='edit_UserToDo'),
    url(r'^UserNote/edit/(?P<pk>[\w-]+)/$', EditUserNoteView.as_view(), name='edit_UserNote'),
    url(r'^NoteDescription/edit/(?P<pk>[\w-]+)/$', EditNoteDescriptionView.as_view(), name='edit_NoteDescription'),
    url(r'^handleHomePagination/?$', HandleHomePagination.as_view(), name='home_handlePagination'),
]