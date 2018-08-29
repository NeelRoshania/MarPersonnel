from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ImproperlyConfigured
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from production.forms import ProductionMeetingForm, ProductionNoteForm, RMShortageForm, MaintenanceIssueForm, ProductionPlanForm
from sales.forms import DeliveryPlanForm, CustomerIDForm
from home.models import UserToDo, UserNote
from production.models import ProdMeeting, ProdNote, RMShortage, RMReference, MaintenanceIssue, ProductionPlan
from sales.models import DeliveryPlan, CustomerID

class AjaxFormMixin_Sales(object):

    # Update the object if form is in-valid
    def form_invalid_sales(self, form):
        print("AjaxFormMixin_Sales:form_invalid_sales called. ")
        response = super(AjaxFormMixin_Sales, self).form_invalid(form)
        if self.request.is_ajax():
            print('{}{}'.format("Form Errors: ", form.errors))
            return JsonResponse({'error': [{"field":k, "message": v[0]} for k, v in form.errors.items()]}, status=400)
        else:
            return response

    # Update the object if form is valid
    def form_valid_sales(self, form):
        print("AjaxFormMixin_Sales:form_valid_sales called. ")
        response = super(AjaxFormMixin_Sales, self).form_valid(form)
        print('{}{}'.format("AjaxFormMixin_Sales form_valid_sales ajaxStatus: ", self.request.POST.get('ajaxStatus')))
        print('{}{}'.format("AjaxFormMixin_Sales form_valid_sales request method: ", self.request.method))
        return self.handleAjax(
            self.request,
            form,
            response,
            )

    # This method was writted to override get_context_data to pass additional context data to the view via ajax
    def get_context_data(self, **kwargs):
        print("Cookie: " + settings.CSRF_COOKIE_NAME)
        print("AjaxFormMixin_Sales:get_context_data called.")
        context = super(AjaxFormMixin_Sales, self).get_context_data(**kwargs)
        # paginator = Paginator(self.getQuerySet_Sales(UserToDo), 5) # Show 5 contacts per page
        salesPage = self.request.GET.get('salesPage') # Get page from ajax request
        obj = DeliveryPlan

        print("AjaxFormMixin_Sales:get_context_data called -> request to get general context")
        formInstances = {
            'deliveryPlan_Form': DeliveryPlanForm(auto_id='DeliveryPlanForm_%s'), 
            'customerID_Form': CustomerIDForm(auto_id='CustomerIDForm_%s'),
            'deliveryPlan_Form': DeliveryPlanForm(auto_id='DeliveryPlanForm_%s'), 
        }
        return self.processPaginatorContext_Sales(Paginator(self.getQuerySet_Sales(obj), 5), formInstances, salesPage, context)

    def getQuerySet_Sales(self, model, pk=None):
        # If the QuerySet requires a pk
        if pk:
            return get_object_or_404(model, pk=self.kwargs['pk'])
        else:
            return model.objects.order_by('-id')

    def processPaginatorContext_Sales(self, paginatorObject, formInstances, page, context):
        print("Time to paginate sales")
        try:
            paginatedObjects = paginatorObject.page(page)
            contextData = {**formInstances, 'paginated_Sales':paginatedObjects}
            context.update(contextData)
            print('{}{}'.format("processPaginatorContext_Sales -> page:", page))
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            paginatedObjects = paginatorObject.page(1)
            contextData = {**formInstances, 'paginated_Sales':paginatedObjects}
            context.update(contextData)
            print('{}{}'.format("processPaginatorContext_Sales PageNotAnInteger -> page:", page))
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            paginatedObjects = paginatorObject.page(paginatorObject.num_pages)
            contextData = {**formInstances, 'paginated_Sales':paginatedObjects}
            context.update(contextData)
            print('{}{}'.format("processPaginatorContext_Sales EmptyPage -> page:", page))

        print('{}{}'.format("AjaxFormMixin_Sales:context: ", context))
        return context

    # Method to detect status of form validation for custom Models
    def handleAjax(self, requestObj, form=None, response=None, model=None):
        print("AjaxFormMixin_Sales:handleAjax called.")
        try:

            if requestObj.is_ajax():
                print("AjaxFormMixin_Sales:Process is ajax.")
                if requestObj.method == 'POST':
                    print("AjaxFormMixin_Sales:Process is POST.")
                    if (requestObj.POST.get('ajaxStatus') == "addDeliveryNoteForm"):
                        try:
                            print("AjaxFormMixin_Sales:handleAjax called -> request to add delivery plan")
                            obj = DeliveryPlan(
                                dateOfDelivery=form.cleaned_data['dateOfDelivery'],
                                invoiceNumber=form.cleaned_data['invoiceNumber'],
                                orderDate=form.cleaned_data['orderDate'],
                                active=form.cleaned_data['active'],
                                delayField=form.cleaned_data['delayField'],
                                delayReason=form.cleaned_data['delayReason'],
                                customerID=form.cleaned_data['customerID'],
                                )
                            obj.save()
                            obj.generatedBy.add(User.objects.get(id=requestObj.user.id))
                            obj.save()
                            # obj.customerID.add(CustomerID.objects.get(id=form.cleaned_data['customerID']))
                            # obj.save()
                            print("AjaxFormMixin_Sales: addDeliveryNoteForm complete!")
                            return JsonResponse({'message': "Delivery plan inserted!",})
                        except ImproperlyConfigured:
                            print("Something went wrong trying to create a new delivery plan")

                    if (requestObj.POST.get('ajaxStatus') == "addCustomerIDForm"):
                        try:
                            print("AjaxFormMixin_Sales:handleAjax called -> request to add customer ID")
                            obj = CustomerID(
                                customerCode=form.cleaned_data['customerCode'],
                                customerName=form.cleaned_data['customerName'],
                                procurementName=form.cleaned_data['procurementName'],
                                procurementWorkNum=form.cleaned_data['procurementWorkNum'],
                                procurementWorkEmail=form.cleaned_data['procurementWorkEmail'],
                                technicalWorkNum=form.cleaned_data['technicalWorkNum'],
                                technicalName=form.cleaned_data['technicalName'],
                                technicalWorkEmail=form.cleaned_data['technicalWorkEmail'],
                                customerStatus=form.cleaned_data['customerStatus'],
                                customerType=form.cleaned_data['customerType'],
                                )
                            obj.save()
                            obj.generatedBy.add(User.objects.get(id=requestObj.user.id))
                            obj.save()
                            print("AjaxFormMixin_Sales: addCustomerIDForm complete!")
                            return JsonResponse({'message': "New customer inserted!",})
                        except ImproperlyConfigured:
                            print("Something went wrong trying to create a CustomerID")

                    if (requestObj.POST.get('ajaxStatus') == "editDeliveryPlanForm"):
                        print("AjaxFormMixin_Sales:handleAjax called -> request to edit a delivery plan")
                        try:
                            # Get object and modify
                            obj = self.getQuerySet_Sales(DeliveryPlan, pk=self.kwargs['pk'])
                            obj.dateOfDelivery=form.cleaned_data['dateOfDelivery']
                            obj.invoiceNumber=form.cleaned_data['invoiceNumber']
                            obj.active=form.cleaned_data['active']
                            obj.delayField=form.cleaned_data['delayField']
                            obj.delayReason=form.cleaned_data['delayReason']
                            # Remove the current and select the first option from the M2M list
                            obj.customerID=form.cleaned_data['customerID']
                            obj.modifiedBy = User.objects.get(id=requestObj.user.id)
                            obj.save()
                            print("AjaxFormMixin_Sales: editDeliveryPlanForm complete!")
                            return JsonResponse({'message': "Delivery Plan modified!",})
                        except ImproperlyConfigured:
                            print("Something went wrong trying to edit a delivery plan.")

                    if (requestObj.POST.get('ajaxStatus') == "editCustomerIDForm"):
                        print("AjaxFormMixin_Sales:handleAjax called -> request to edit a customerID")
                        try:
                            # Get object and modify
                            obj = self.getQuerySet_Sales(CustomerID, pk=self.kwargs['pk'])
                            obj.customerCode=form.cleaned_data['customerCode']
                            obj.customerName=form.cleaned_data['customerName']
                            obj.procurementName=form.cleaned_data['procurementName']
                            obj.procurementWorkNum=form.cleaned_data['procurementWorkNum']
                            obj.procurementWorkEmail=form.cleaned_data['procurementWorkEmail']
                            obj.technicalWorkNum=form.cleaned_data['technicalWorkNum']
                            obj.technicalName=form.cleaned_data['technicalName']
                            obj.technicalWorkEmail=form.cleaned_data['technicalWorkEmail']
                            obj.customerStatus=form.cleaned_data['customerStatus']
                            obj.modifiedBy = User.objects.get(id=requestObj.user.id)
                            obj.save()
                            print("AjaxFormMixin_Sales: editCustomerIDForm complete!")
                            return JsonResponse({'message': "Customer details modified!",})
                        except ImproperlyConfigured:
                            print("Something went wrong trying to edit a customerID.")

            else:
                print("AjaxFormMixin_Sales:handleAjax called -> Neither ajax nor form submit...")
                return response

        except ImproperlyConfigured:
            print("ajaxStatus not properly configured.")

def getSearchObject_Sales(ajaxStatus):
    print('{}{}'.format("getSearchObject_Sales ajaxStatus: ", ajaxStatus))

    if (
        (ajaxStatus == 'search_EDIT_CustomerID') or 
        (ajaxStatus == 'customerIDPaginationNext') or 
        (ajaxStatus == 'customerIDPaginationPrevious')
        ):
        return CustomerID
    
    elif (ajaxStatus == 'search_DeliveryPlans'):
        return DeliveryPlan
    else:
        raise ImproperlyConfigured("POST ajaxStatus not available in getAuthenticationForm")




