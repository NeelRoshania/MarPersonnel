from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from home.models import UserToDo, UserNote, NoteDescription
from .forms import UserToDoForm, UserNoteForm, NoteDescriptionForm

class AjaxFormMixin_Home(object):

    # Update the object if form is in-valid
    def form_invalid_home(self, form):
        print("\n\nAjaxFormMixin_Home:form_invalid_home called. ")
        response = super(AjaxFormMixin_Home, self).form_invalid(form)
        if self.request.is_ajax():
            print("\n\nForm errors: \n\n {}".format(form.errors.as_json()))
            return JsonResponse({'error': [{"field":k, "message": v[0]} for k, v in form.errors.items()]}, status=400)
        else:
            return response

    # Update the object if form is valid
    def form_valid_home(self, form):
        print("\n\nAjaxFormMixin_Home:form_valid_home called. ")
        response = super(AjaxFormMixin_Home, self).form_valid(form)
        print('\n\n{}{}'.format("ajaxStatus: ", self.request.POST.get('ajaxStatus')))
        print('\n\n{}{}'.format("request method: ", self.request.method))
        return self.handleAjax(
            self.request,
            form,
            response,
            )

    # This method was writted to override that of UserToDoFormView method -> context data is not being passed to form
    def get_context_data(self, **kwargs):
        print("\n\nCookie: " + settings.CSRF_COOKIE_NAME)
        print("\n\nAjaxFormMixin_Home:get_context_data called.")
        context = super(AjaxFormMixin_Home, self).get_context_data(**kwargs)
        # paginator = Paginator(self.getQuerySet(UserToDo), 5) # Show 5 contacts per page
        userToDoPage = self.request.GET.get('userToDoPage') # Get page from ajax request
        obj = UserToDo.objects.filter(generatedBy=self.request.user, toDoProgress='In Progress').order_by('insertedAt')
        
        print("\n\nAjaxFormMixin_Home:get_context_data called -> request to get general context")
        formInstances = {
            'userToDo_Form': UserToDoForm(auto_id='userToDoForm_%s'),
            'userNote_Form': UserNoteForm(auto_id='userNoteForm_%s'),
            'noteDescription_Form': NoteDescriptionForm(auto_id='noteDescriptionForm_%s'),
        }
        return self.processPaginatorContext(Paginator(obj, 5), formInstances, userToDoPage, context)

    def getQuerySet(self, model, pk=None):
        # If the QuerySet requires a pk
        if pk:
            return get_object_or_404(model, pk=self.kwargs['pk'])
        else:
            return model.objects.order_by('-id')

    def processPaginatorContext(self, paginatorObject, formInstances, page, context):
        print("\n\nTime to paginate production")
        try:
            paginatedObjects = paginatorObject.page(page)
            contextData = {**formInstances, 'paginatedUserToDos':paginatedObjects}
            context.update(contextData)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            paginatedObjects = paginatorObject.page(1)
            contextData = {**formInstances, 'paginatedUserToDos':paginatedObjects}
            context.update(contextData)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            paginatedObjects = paginatorObject.page(paginatorObject.num_pages)
            contextData = {**formInstances, 'paginatedUserToDos':paginatedObjects}
            context.update(contextData)

        print('\n\n{}{}'.format("AjaxFormMixin_Home:context: ", context))
        return context

    # Method to detect status of form validation for custom Models
    def handleAjax(self, requestObj, form=None, response=None, model=None):
        print("\n\nAjaxFormMixin_Home:handleAjax called.")
        try:

            if requestObj.is_ajax():
                print("\n\nAjaxFormMixin_Home:Process is ajax.")
                if requestObj.method == 'POST':
                    if (requestObj.POST.get('ajaxStatus') == "addUserToDoForm"):
                        print("\n\nAjaxFormMixin_Home:handleAjax called -> request to add UserToDo")
                        print("Authenticated user id: {}".format(requestObj.user.id))
                        obj = UserToDo(
                            subject=form.cleaned_data['subject'], 
                            toDoProgress=form.cleaned_data['toDoProgress'],
                            )
                        obj.save()
                        obj.generatedBy.add(User.objects.get(id=requestObj.user.id))
                        obj.save()
                        return JsonResponse({'message': "You have new objectives!",})

                    if (requestObj.POST.get('ajaxStatus') == "addUserNoteForm"):
                        print("\n\nAjaxFormMixin_Home:handleAjax called -> request to add UserNote")
                        # Get object and modify
                        print("\n\nuserToDo Object: ", get_object_or_404(UserToDo, pk=requestObj.POST.get('userToDo')))
                        obj = UserNote(
                            taskNote=form.cleaned_data['taskNote'], 
                            noteProgress=form.cleaned_data['noteProgress'],
                        )                   
                        obj.save()
                        obj.UserToDo.add(UserToDo.objects.get(id=requestObj.POST.get('userToDo')))
                        obj.generatedBy.add(User.objects.get(id=requestObj.user.id))
                        obj.save()
                        return JsonResponse({'message': "Sub-objective inserted!",})
                    
                    if (requestObj.POST.get('ajaxStatus') == "addNoteDescriptionForm"):
                        print("\n\nAjaxFormMixin_Home:handleAjax called -> request to add Note Description")
                        # Get object and modify
                        print("\n\nUserNote Object: ", get_object_or_404(UserNote, pk=requestObj.POST.get('userNote')))
                        obj = NoteDescription(
                            description=form.cleaned_data['description'],
                            noteDescriptionProgress=form.cleaned_data['noteDescriptionProgress'],
                            userNote=UserNote.objects.get(id=requestObj.POST.get('userNote'))
                        )                   
                        obj.save()
                        obj.generatedBy.add(User.objects.get(id=requestObj.user.id))
                        obj.save()
                        return JsonResponse({'message': "Sub-objective task inserted!",})

                    if (requestObj.POST.get('ajaxStatus') == "editUserToDoForm"):
                        print("\n\nAjaxFormMixin_Home:handleAjax called -> request to edit user to do")
                        # Get object and modify
                        obj = self.getQuerySet(UserToDo, pk=self.kwargs['pk'])
                        obj.subject = form.cleaned_data['subject']
                        obj.toDoProgress = form.cleaned_data['toDoProgress']
                        obj.modifiedBy = User.objects.get(id=requestObj.user.id)
                        obj.save()
                        return JsonResponse({'message': "Modified!"})

                    if (requestObj.POST.get('ajaxStatus') == "editUserNoteForm"):
                        print("\n\nAjaxFormMixin_Home:handleAjax called -> request to edit user note")
                        # Get object and modify
                        obj = self.getQuerySet(UserNote, pk=self.kwargs['pk'])
                        obj.noteProgress = form.cleaned_data['noteProgress']
                        obj.taskNote = form.cleaned_data['taskNote']
                        obj.modifiedBy = User.objects.get(id=requestObj.user.id)
                        obj.save()

                        # Need to think about this one!
                        return JsonResponse({'message': "Modified!",})

                    if (requestObj.POST.get('ajaxStatus') == "editNoteDescriptionForm"):
                        print("\n\nAjaxFormMixin_Home:handleAjax called -> request to edit note description")
                        # Get object and modify
                        obj = self.getQuerySet(NoteDescription, pk=self.kwargs['pk'])     
                        # print("\n\nobject ->" + str(author.name))
                        # print("\n\nmodified ->" + str(form.cleaned_data['name']))
                        obj.description = form.cleaned_data['description']
                        obj.noteDescriptionProgress=form.cleaned_data['noteDescriptionProgress']
                        obj.modifiedBy = User.objects.get(id=requestObj.user.id)
                        obj.save()
                        return JsonResponse({'message': "Modified!",})
                else:

                    return JsonResponse({"message" : "Something went wrong, call the administrator!"});
            else:
                print("\n\nAjaxFormMixin_Home:handleAjax called -> Neither ajax nor form submit...")
                return response

        except ImproperlyConfigured:
            print("\n\najaxStatus not properly configured.")


