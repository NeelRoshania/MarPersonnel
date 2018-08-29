from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import FormView, View, ListView
from django.views.generic.base import TemplateView, TemplateResponseMixin
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ImproperlyConfigured
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.edit import FormMixin, ContextMixin
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from .forms import UserToDoForm, UserNoteForm, NoteDescriptionForm, LoginForm
from home.mixins import AjaxFormMixin_Home
from production.mixins import AjaxFormMixin_Production
from sales.mixins import AjaxFormMixin_Sales
from quality.mixins import AjaxFormMixin_Quality
from .models import UserToDo, UserNote, NoteDescription
from urllib import parse
import traceback

class UserLoginView(View):
    form_class = LoginForm
    template_name = 'login_form.html'

    #Display a blank form - no context passed it "None" & pass the form class to the template_name
    def get(self, request):
        form = self.form_class(None)
        request.session['LoginStatus'] = 'To_LogIn'
        return render(request, self.template_name, {'form':form,})

    # Process form data on submit
    def post(self, request):
        print("UserLoginView: Login attempt")
        form = self.form_class(request.POST)
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        print("User authentication status: {}".format(user))
        # If the user is authenticated
        if user is not None:
            print("UserLoginView: Login pass")
            if user.is_active:
                request.session['LoginStatus'] = 'userActive'
                login(request, user)
                return JsonResponse({"url" : "/"})
        else:
            print("UserLoginView: Login Fail")
            return JsonResponse({"errorMessage" : "Username or passord incorrect!"})

class UserLogoutView(View):
    template_name = 'login_form.html'
    
    #Display a blank form - no context passed it "None" & pass the form class to the template_name
    def get(self, request):
        request.session['LoginStatus'] = 'To_LogOut'
        logout(request)
        return render(request, self.template_name)

# Home view to redirect user
class BaseView(LoginRequiredMixin, AjaxFormMixin_Home, AjaxFormMixin_Production, AjaxFormMixin_Sales, AjaxFormMixin_Quality, FormMixin, TemplateResponseMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    success_url = reverse_lazy('home:index')
    template_name  = 'home/home.html'

    # get request for home page -> return context from AjaxFormMixin_Home by overiding parent class + define auto_id for generated fields
    def get(self, request, *args, **kwargs):
        print("\n\nBaseView Home: GET request called. ")
        self.form_class = UserToDoForm
        # context = super(BaseView, self).get_context_data(**kwargs)
        context = self.get_context_data(**kwargs)
        context.update({
                    'userToDo_Form': UserToDoForm(auto_id='userToDoForm_%s'),
                    'userNote_Form': UserNoteForm(auto_id='userNoteForm_%s'),
                    'noteDescription_Form': NoteDescriptionForm(auto_id='noteDescriptionForm_%s'),
                     })
        print('\n\n{}{}'.format("context:", context))
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):   
        print("\n\nBaseView Home: POST request called. ")
        # Decide validation form class
        if (request.POST.get('ajaxStatus') == 'addUserNoteForm'):
            self.form_class = UserNoteForm
        elif (request.POST.get('ajaxStatus') == 'addNoteDescriptionForm'):
            self.form_class = NoteDescriptionForm
        else:
            self.form_class = UserToDoForm

        form = self.get_form()
        if form.is_valid():
            return self.form_valid_home(form)
        else:
            return self.form_invalid_home(form)

# RefershUserToDoView -> TemplateView handles render_to_responce, which returns an HTTPResponse 
class RefershUserToDoView(AjaxFormMixin_Home, TemplateView):
    template_name = 'home/includes/objectList.html'

# DeleteUserToDoView does not need to return a template. As AJAX, it just needs to post data to the database and return a Jsonresponse
class DeleteModelView(View):

    # @method_decorator(ensure_csrf_cookie) -> Does not assist with AJAX requests
    def post(self, request, *args, **kwargs):
        print("\n\nhome DeleteModel: POST request called to delete object. ")
        print('\n\n{}{}{}{}'.format("ajaxStatus: ", request.POST.get('ajaxStatus'), " pk: ", self.kwargs['pk']))
        return self.deleteObject(request.POST.get('ajaxStatus'), self.kwargs['pk'])

    def deleteObject(self, ajaxStatus, pk):
        print('\n\n{}{}'.format("ajaxStatus: ", ajaxStatus))
        try:
            if (ajaxStatus=="deleteUserToDo"):
                _ = get_object_or_404(UserToDo, pk=pk)
                print('\n\n{}{}'.format("Object to delete: ", _))
                _.delete()
                return JsonResponse({"message": 'Objective deleted succesfully.'}) 

            elif (ajaxStatus=="deleteUserNote"):
                _ = get_object_or_404(UserNote, pk=pk)
                print('\n\n{}{}'.format("Object to delete: ", _))
                _.delete()
                return JsonResponse({"message": 'Task deleted succesfully.'})

            elif (ajaxStatus=="deleteNoteDescriptionForm"):
                _ = get_object_or_404(NoteDescription, pk=pk)
                print('\n\n{}{}'.format("Object to delete: ", _))
                _.delete()
                return JsonResponse({"message": 'Note deleted succesfully.'})
                
            else:
                return JsonResponse({"message": 'Object deleted succesfully.'})

        except:
            traceback.print_exc()
            return JsonResponse({"message": 'Oops! Looks like something went wrong, contact your administrator!'})

# EditUserToDoView must generate a tempalte with a form to pass object information to
class EditUserToDoView(AjaxFormMixin_Home, FormMixin, TemplateResponseMixin, View):
    form_class = UserToDoForm
    success_url = reverse_lazy('home:index')
    template_name = 'home/includes/editUserToDo.html'

    # get data from database -> different from get_context_data as it does not return an HTTPResponse
    def get(self, request, *args, **kwargs):
        print("\n\nHome EditUserToDoView: GET request called. ")
        print("\n\npk: " + self.kwargs['pk'])

        # Get author object and form instance and return from instance to view
        obj = get_object_or_404(UserToDo, pk=self.kwargs['pk'])
        form = UserToDoForm(instance=obj, auto_id='editUserToDo_%s')
        return self.render_to_response({'subForm': form})

    # Post data to database
    def post(self, request, *args, **kwargs):
        print("\n\nhome EditUserToDoView: POST request called. ")

        form = self.get_form()
        if form.is_valid():
            return self.form_valid_home(form)
        else:
            return self.form_invalid_home(form)

# EditUserNoteView must generate a tempalte with a form to pass object information to
class EditUserNoteView(AjaxFormMixin_Home, FormMixin, TemplateResponseMixin, View):
    form_class = UserNoteForm
    success_url = reverse_lazy('home:index')
    template_name = 'home/includes/editUserNoteForm.html'

    # get data from database -> different from get_context_data as it does not return an HTTPResponse
    def get(self, request, *args, **kwargs):
        print("\n\nHome EditUserNoteView: GET request called. ")
        print("\n\npk: " + self.kwargs['pk'])

        # Get author object and form instance and return from instance to view
        obj = get_object_or_404(UserNote, pk=self.kwargs['pk'])
        form = UserNoteForm(instance=obj, auto_id='editUserNote_%s')
        return self.render_to_response({'subForm': form})

    # Post data to database
    def post(self, request, *args, **kwargs):
        print("\n\nhome EditUserNoteView: POST request called. ")

        form = self.get_form()
        if form.is_valid():
            return self.form_valid_home(form)
        else:
            return self.form_invalid_home(form)

# EditUserNoteView must generate a tempalte with a form to pass object information to
class EditNoteDescriptionView(AjaxFormMixin_Home, FormMixin, TemplateResponseMixin, View):
    form_class = NoteDescriptionForm
    success_url = reverse_lazy('home:index')
    template_name = 'home/includes/editNoteDescriptionForm.html'

    # get data from database -> different from get_context_data as it does not return an HTTPResponse
    def get(self, request, *args, **kwargs):
        print("\n\nHome EditUserNoteView: GET request called. ")
        print("\n\npk: " + self.kwargs['pk'])

        # Get author object and form instance and return from instance to view
        obj = get_object_or_404(NoteDescription, pk=self.kwargs['pk'])
        form = NoteDescriptionForm(instance=obj, auto_id='editNoteDescriptionForm_%s')
        return self.render_to_response({'subForm': form})

    # Post data to database
    def post(self, request, *args, **kwargs):
        print("\n\nhome EditNoteDescriptionView: POST request called. ")

        form = self.get_form()
        if form.is_valid():
            return self.form_valid_home(form)
        else:
            return self.form_invalid_home(form)

# SearchObjectView must generate a tempalte to pass context objects to
class SearchUserToDoView(AjaxFormMixin_Home, TemplateView):
    template_name = 'home/includes/objectList.html'

# Pagination view to handle general pagination requests and search requests
class HandleHomePagination(AjaxFormMixin_Home, ContextMixin, View):
        template_name = 'home/includes/objectList.html'

        # A pagination request is made here
        def get(self, request, *args, **kwargs):
            print("\n\nHome HandlePagination: GET request called. ")
            print('\n\n{}{}'.format("Home HandlePagination: ajaxStatus -> ", request.GET.get('ajaxStatus')))
            print('\n\n{}{}'.format("Home HandlePagination: searchObjectFieldText -> ", request.GET.get('searchObjectFieldText')))
            print('\n\n{}{}'.format("Home HandlePagination: searchHomePage -> ", request.GET.get('searchHomePage')))

            # User searches for a DeliveryPlan
            searchText = self.request.GET.get('searchObjectFieldText')
            if searchText is None:
                searchText = " "

            # Call context data to make forms available after search
            context = super(HandleHomePagination, self).get_context_data(**kwargs)

            print('\n\nHandleHomePagination:searchText -> {}'.format(searchText))
            
            try:
                # Search for a UserToDo
                if (request.GET.get('ajaxStatus') == "searchUserToDo"):
                    print("\n\nHandleHomePagination: -> request to search for subject of UserToDo")
                    print('\n\n{}{}'.format("searchText for DeliveryPlan: ", searchText))
                    print('\n\n{}{}'.format("requestType: ", request.GET.get('requestType')))

                    if (self.request.GET.get('requestType') == "subject" ) or (self.request.GET.get('radio') == "subject"):
                        print("\n\nHandleHomePagination: -> request to search for a customer")
                        context.update({"paginatedUserToDos" : Paginator(UserToDo.objects.filter(subject__contains=searchText), 5).page(request.GET.get('searchHomePage'))})
                        return render(
                            request,
                            self.template_name,
                            context)
                    
                    elif (self.request.GET.get('requestType') == "progress" ) or (self.request.GET.get('radio') == "progress"):
                        print("\n\nHandleHomePagination: -> request to search progress of UserToDo")
                        context.update({"paginatedUserToDos" : Paginator(UserToDo.objects.filter(toDoProgress__contains=searchText), 5).page(request.GET.get('searchHomePage'))})
                        return render(
                            request,
                            self.template_name,
                            context)

                    else: 
                        return JsonResponse({"message" : "Select a filter!"});
                
                elif (request.GET.get('ajaxStatus') == 'searchUserNote'):
                    print("\n\nHandleHomePagination: -> request to paginate UserNote search results")
                    print('\n\n{}{}'.format("searchText for UserNote: ", searchText))
                    print('\n\n{}{}'.format("requestType: ", request.GET.get('requestType')))
                        
                    if (self.request.GET.get('requestType') == "progress" ) or (self.request.GET.get('radio') == "progress"):
                        print("\n\nHandleHomePagination: -> request to search for a customer")
                        context.update({"paginatedUserToDos" : Paginator(UserToDo.objects.filter(usernote__in=UserNote.objects.filter(noteProgress__contains=searchText)).distinct(), 5).page(request.GET.get('searchHomePage'))})
                        return render(
                            request,
                            self.template_name,
                            context)
                    
                    elif (self.request.GET.get('requestType') == "note" ) or (self.request.GET.get('radio') == "note"):
                        print("\n\nHandleHomePagination: -> request to search progress of UserToDo")
                        context.update({"paginatedUserToDos" : Paginator(UserToDo.objects.filter(usernote__in=UserNote.objects.filter(taskNote__contains=searchText)).distinct(), 5).page(request.GET.get('searchHomePage'))})
                        return render(
                            request,
                            self.template_name,
                            context)

                    else: 
                        return JsonResponse({"message" : "Select a filter!"});

                elif (request.GET.get('ajaxStatus') == 'searchNoteDescription'):
                    print("\n\nHandleHomePagination: -> request to paginate NoteDescription results")
                    print('\n\n{}{}'.format("searchText for NoteDescription: ", searchText))
                    print('\n\n{}{}'.format("requestType: ", request.GET.get('requestType')))
                        
                    if (self.request.GET.get('requestType') == "progress" ) or (self.request.GET.get('radio') == "progress"):
                        print("\n\nHandleHomePagination: -> request to search for a progress on Note Description")
                        context.update({"paginatedUserToDos" : Paginator(UserNote.objects.filter(noteDescription__in=NoteDescription.objects.filter(noteDescriptionProgress__contains=searchText)).distinct(), 5).page(request.GET.get('searchHomePage'))})
                        return render(
                            request,
                            self.template_name,
                            context)
                    
                    elif (self.request.GET.get('requestType') == "description" ) or (self.request.GET.get('radio') == "description"):
                        print("\n\nHandleHomePagination: -> request to search description of NoteDescription")
                        context.update({"paginatedUserToDos" : Paginator(UserToDo.objects.filter(noteDescription__in=NoteDescription.objects.filter(description__contains=searchText)).distinct(), 5).page(request.GET.get('searchHomePage'))})
                        return render(
                            request,
                            self.template_name,
                            context)
                    else: 
                        return JsonResponse({"message" : "Select a filter!"});

                else: 
                        return JsonResponse({"message" : "Select a filter!"});

            except :
                traceback.print_exc()
                return JsonResponse({"errorMessage" : "Invalid search procedure! Contact the administrator!"})

