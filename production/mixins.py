from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ImproperlyConfigured
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from .forms import ProductionMeetingForm, ProductionNoteForm, RMShortageForm, MaintenanceIssueForm, ProductionPlanForm, RMReferenceForm
from home.models import UserToDo, UserNote
from production.models import ProdMeeting, ProdNote, RMShortage, RMReference, MaintenanceIssue, ProductionPlan

class AjaxFormMixin_Production(object):

    # Update the object if form is in-valid
    def form_invalid_production(self, form):
        print("AjaxFormMixin_Production:form_invalid_production called. ")
        response = super(AjaxFormMixin_Production, self).form_invalid(form)
        if self.request.is_ajax():
            print('{}{}'.format("Form Errors: ", form.errors))
            return JsonResponse({'error': [{"field":k, "message": v[0]} for k, v in form.errors.items()]}, status=400)
        else:
            return response

    # Update the object if form is valid
    def form_valid_production(self, form):
        print("AjaxFormMixin_Production:form_valid_production called. ")
        response = super(AjaxFormMixin_Production, self).form_valid(form)
        print('{}{}'.format("AjaxFormMixin_Production form_valid_production ajaxStatus: ", self.request.POST.get('ajaxStatus')))
        print('{}{}'.format("AjaxFormMixin_Production form_valid_production request method: ", self.request.method))
        return self.handleAjax(
            self.request,
            form,
            response,
            )

    # This method was writted to override that of UserToDoFormView method -> context data is not being passed to form
    def get_context_data(self, **kwargs):
        print("Cookie: " + settings.CSRF_COOKIE_NAME)
        print("AjaxFormMixin_Production:get_context_data called.")
        context = super(AjaxFormMixin_Production, self).get_context_data(**kwargs)
        # paginator = Paginator(self.getQuerySet_Production(UserToDo), 5) # Show 5 contacts per page
        productionPage = self.request.GET.get('productionPage') # Get page from ajax request
        obj = ProdMeeting
        print("AjaxFormMixin_Production:get_context_data called -> request to get general context")
        
        formInstances = {
            'productionMeeting_Form': ProductionMeetingForm(auto_id='ProductionMeetingForm_%s'),
            'productionNote_Form': ProductionNoteForm(auto_id='ProductionNoteForm_%s'),
            'rmShortage_Form': RMShortageForm(auto_id='rmShortage_Form_%s'),
            'maintenanceIssue_Form': MaintenanceIssueForm(auto_id='maintenanceIssue_Form_%s'),
            'ProductionPlan_Form': ProductionPlanForm(auto_id='ProductionPlan_Form_%s'),
            'RMReference_Form': RMReferenceForm(auto_id='RMReference_Form_%s'),
            'rRMReference': RMReference.objects.all()
        }
        return self.processPaginatorContext_Production(Paginator(self.getQuerySet_Production(obj), 5), formInstances, productionPage, context)

    def getQuerySet_Production(self, model, pk=None):
        # If the QuerySet requires a pk
        if pk:
            return get_object_or_404(model, pk=self.kwargs['pk'])
        else:
            return model.objects.order_by('-id')

    def processPaginatorContext_Production(self, paginatorObject, formInstances, page, context):
        print("Time to paginate production")
        try:
            paginatedObjects = paginatorObject.page(page)
            contextData = {**formInstances, 'paginated_Production':paginatedObjects}
            context.update(contextData)
            print('{}{}'.format("processPaginatorContext_Production -> productionPage:", page))
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            paginatedObjects = paginatorObject.page(1)
            contextData = {**formInstances, 'paginated_Production':paginatedObjects}
            context.update(contextData)
            print('{}{}'.format("processPaginatorContext_Production PageNotAnInteger -> productionPage:", page))
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            paginatedObjects = paginatorObject.page(paginatorObject.num_pages)
            contextData = {**formInstances, 'paginated_Production':paginatedObjects}
            context.update(contextData)
            print('{}{}'.format("processPaginatorContext_Production EmptyPage -> productionPage:", page))

        print('{}{}'.format("AjaxFormMixin_Production:context: ", context))
        return context

    # Method to detect status of form validation for custom Models
    def handleAjax(self, requestObj, form=None, response=None, model=None):
        print("AjaxFormMixin_Production:handleAjax called.")
        try:

            if requestObj.is_ajax():
                print("AjaxFormMixin_Production:Process is ajax.")
                if requestObj.method == 'POST':
                    if (requestObj.POST.get('ajaxStatus') == "addProductionMeetingForm"):
                        try:
                            print("AjaxFormMixin_Production:handleAjax called -> request to add ProdMeeting")
                            obj = ProdMeeting(
                                subject=form.cleaned_data['subject'], 
                                # toDoProgress=form.cleaned_data['toDoProgress'],
                                )
                            obj.save()
                            obj.generatedBy.add(User.objects.get(id=requestObj.user.id))
                            obj.save()
                            print("AjaxFormMixin_Production: addProductionMeetingForm complete!")
                            return JsonResponse({'message': "Production meeting created!",})
                        except ImproperlyConfigured:
                            return JsonResponse({'message': "Something went wrong trying to create a new production meeting.",})

                    if (requestObj.POST.get('ajaxStatus') == "addProductionNoteForm"):
                        print("AjaxFormMixin_Production:handleAjax called -> request to add Production Note")
                        # Get object and modify
                        print('{}{}{}{}'.format("prodNote: ", form.cleaned_data['prodNote'], " & prodMeeting ID: ", requestObj.POST.get('prodMeeting')))
                        try:
                            obj = ProdNote(
                                prodNote=form.cleaned_data['prodNote'], 
                                # noteProgress=form.cleaned_data['noteProgress'],
                            )                   
                            obj.save()
                            obj.productionMeeting.add(ProdMeeting.objects.get(id=requestObj.POST.get('prodMeeting')))
                            obj.generatedBy.add(User.objects.get(id=requestObj.user.id))
                            obj.save()
                            print("AjaxFormMixin_Production: addProductionNoteForm complete!")
                            return JsonResponse({'message': "Production note created!",})
                        except ImproperlyConfigured:
                            return JsonResponse({'message': "Something went wrong trying to create a new production Note.",})
                        
                    if (requestObj.POST.get('ajaxStatus') == "addRMSHortageForm"):
                        print("AjaxFormMixin_Production:handleAjax called -> request to add RMShortage")
                        try:
                            obj = RMShortage(
                                # rmShortage=form.cleaned_data['rmShortage'], 
                                rmLevel=form.cleaned_data['rmLevel'], 
                                rmStatus=form.cleaned_data['rmStatus'],
                                # toDoProgress=form.cleaned_data['toDoProgress'],
                                )
                            obj.save()
                            obj.productionMeeting.add(ProdMeeting.objects.get(id=requestObj.POST.get('prodMeeting')))
                            obj.rmShortage.add(RMReference.objects.get(id=requestObj.POST.get('rmShortage')))
                            obj.generatedBy.add(User.objects.get(id=requestObj.user.id))
                            obj.save()
                            print("AjaxFormMixin_Production: addRMSHortageForm complete!")
                            return JsonResponse({'message': "Raw material shortage created!",})
                        except ImproperlyConfigured:
                            print("Something went wrong trying to create a new production Note")

                    if (requestObj.POST.get('ajaxStatus') == "addMaintenanceIssueForm"):
                        print("AjaxFormMixin_Production:handleAjax called -> request to add rmShortage")
                        try:
                            obj = MaintenanceIssue(
                                # rmShortage=form.cleaned_data['rmShortage'], 
                                maintenanceType=form.cleaned_data['maintenanceType'], 
                                subject=form.cleaned_data['subject'],
                                note=form.cleaned_data['note'],
                                active=form.cleaned_data['active'],
                                # toDoProgress=form.cleaned_data['toDoProgress'],
                                )
                            obj.save()
                            obj.productionMeeting.add(ProdMeeting.objects.get(id=requestObj.POST.get('prodMeeting')))
                            obj.generatedBy.add(User.objects.get(id=requestObj.user.id))
                            obj.save()
                            print("AjaxFormMixin_Production: addMaintenanceIssueForm complete!")
                            return JsonResponse({'message': "Maintenance issue created!",})
                        except ImproperlyConfigured:
                            print("Something went wrong trying to create a new MaintenanceIssue")

                    if (requestObj.POST.get('ajaxStatus') == "addProductionPlanForm"):
                        print("AjaxFormMixin_Production:handleAjax called -> request to add Production Plan")
                        # Get object and modify
                        try:
                            obj = ProductionPlan(
                                machine=form.cleaned_data['machine'], 
                                batchNumber=form.cleaned_data['batchNumber'],
                                productDescription=form.cleaned_data['productDescription'],
                                status=form.cleaned_data['status'],
                                # noteProgress=form.cleaned_data['noteProgress'],
                            )
                            obj.save()
                            obj.productionMeeting.add(ProdMeeting.objects.get(id=requestObj.POST.get('prodMeeting')))
                            obj.generatedBy.add(User.objects.get(id=requestObj.user.id))
                            obj.save()
                            print("AjaxFormMixin_Production: addProductionPlanForm complete!")
                            return JsonResponse({'message': "Production plan created!",})
                        except ImproperlyConfigured:
                            print("Something went wrong trying to create a new ProductionPlan")

                    if (requestObj.POST.get('ajaxStatus') == "addRM_Reference"):
                        print("AjaxFormMixin_Production:handleAjax called -> request to add a RM Reference")
                        # Get object and modify
                        try:
                            obj = RMReference(
                                rmCode=form.cleaned_data['rmCode'], 
                                rmDescription=form.cleaned_data['rmDescription'],
                                modifiedBy=User.objects.get(id=requestObj.user.id)
                            )
                            obj.save()
                            obj.generatedBy.add(User.objects.get(id=requestObj.user.id))
                            obj.save()
                            print("AjaxFormMixin_Production: addProductionPlanForm complete!")
                            return JsonResponse({'message': "Raw material created!",})
                        except ImproperlyConfigured:
                            print("Something went wrong trying to create a new raw material")

                    if (requestObj.POST.get('ajaxStatus') == "editProductionMeetingForm"):
                        print("AjaxFormMixin_Production:handleAjax called -> request to edit Production Meeting")
                        try:
                            # Get object and modify
                            obj = self.getQuerySet_Production(ProdMeeting, pk=self.kwargs['pk'])
                            obj.subject = form.cleaned_data['subject']
                            obj.modifiedBy = User.objects.get(id=requestObj.user.id)
                            obj.save()
                            print("AjaxFormMixin_Production: editProductionMeetingForm complete!")
                            return JsonResponse({'message': "Meeting edited!",})
                        except ImproperlyConfigured:
                            print("Something went wrong trying to edit a production meeting.")

                    if (requestObj.POST.get('ajaxStatus') == "editRawMaterial"):
                        print("AjaxFormMixin_Production:handleAjax called -> request to edit a RM Reference")
                        # Get object and modify
                        try:
                            obj = self.getQuerySet_Production(RMReference, pk=self.kwargs['pk'])
                            obj.rmCode = form.cleaned_data['rmCode']
                            obj.rmDescription = form.cleaned_data['rmDescription']
                            obj.modifiedBy = User.objects.get(id=requestObj.user.id)
                            obj.save()
                            print("AjaxFormMixin_Production: editRawMaterial complete!")
                            return JsonResponse({'message': "Raw material modified!",})
                        except ImproperlyConfigured:
                            print("Something went wrong trying to modify a new raw material")

                    if (requestObj.POST.get('ajaxStatus') == "editRMShortageForm"):
                        print("AjaxFormMixin_Production:handleAjax called -> request to edit Raw Material Shortage")
                        # Get object and modify 
                        try:
                            obj = self.getQuerySet_Production(RMShortage, pk=self.kwargs['pk'])
                            obj.rmShortage = form.cleaned_data['rmShortage']
                            obj.rmLevel = form.cleaned_data['rmLevel']
                            obj.rmStatus = form.cleaned_data['rmStatus']
                            obj.modifiedBy = User.objects.get(id=requestObj.user.id)
                            obj.save()
                            return JsonResponse({'message': "Raw material shortage changed!",})
                        except ImproperlyConfigured:
                            print("Something went wrong trying to edit a production meeting.")
                        return response

                    if (requestObj.POST.get('ajaxStatus') == "editProductionNoteForm"):
                        print("AjaxFormMixin_Production:handleAjax called -> request to edit Prod Note")
                        try:
                            # Get object and modify
                            obj = self.getQuerySet_Production(ProdNote, pk=self.kwargs['pk'])
                            obj.prodNote = form.cleaned_data['prodNote']
                            obj.modifiedBy = User.objects.get(id=requestObj.user.id)
                            obj.save()
                            return JsonResponse({'message': "Production note edited!",})
                        except ImproperlyConfigured:
                            print("Something went wrong trying to edit a production note.")

                    if (requestObj.POST.get('ajaxStatus') == "editMaintenanceIssueForm"):
                        print("AjaxFormMixin_Production:handleAjax called -> request to edit Maintenance ISsue")
                        try:
                            # Get object and modify
                            obj = self.getQuerySet_Production(MaintenanceIssue, pk=self.kwargs['pk'])    
                            obj.maintenanceType=form.cleaned_data['maintenanceType']
                            obj.subject=form.cleaned_data['subject']
                            obj.note=form.cleaned_data['note']
                            obj.active=form.cleaned_data['active']
                            obj.modifiedBy = User.objects.get(id=requestObj.user.id)
                            obj.save()
                            return JsonResponse({'message': "Maintenance issue edited!",})
                        except ImproperlyConfigured:
                            print("Something went wrong trying to edit a production note.")

                    if (requestObj.POST.get('ajaxStatus') == "editProductionPlanForm"):
                        print("AjaxFormMixin_Production:handleAjax called -> request to edit Production Plan")
                        try:
                            # Get object and modify
                            obj = self.getQuerySet_Production(ProductionPlan, pk=self.kwargs['pk'])    
                            obj.machine=form.cleaned_data['machine']
                            obj.batchNumber=form.cleaned_data['batchNumber']
                            obj.productDescription=form.cleaned_data['productDescription']
                            obj.status=form.cleaned_data['status']
                            obj.modifiedBy = User.objects.get(id=requestObj.user.id)
                            obj.save()
                            return JsonResponse({'message': "Production plan edited!",})
                        except ImproperlyConfigured:
                            print("Something went wrong trying to edit a production note.")

            else:
                print("AjaxFormMixin_Production:handleAjax called -> Neither ajax nor form submit...")
                return response

        except ImproperlyConfigured:
            print("ajaxStatus not properly configured.")




