from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.generic.base import TemplateView, TemplateResponseMixin, ContextMixin
from django.views.generic import FormView, View, ListView
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.http import JsonResponse
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from sales.mixins import AjaxFormMixin_Sales
from sales.models import DeliveryPlan, CustomerID
from .forms import DeliveryPlanForm, CustomerIDForm
from datetime import datetime
import traceback

# Create your views here.

# Home view to redirect user
class BaseView(AjaxFormMixin_Sales, FormMixin, TemplateResponseMixin, View):
    success_url = reverse_lazy('home:index')
    template_name  = 'home/home.html'

    # get request for home page -> return context from AjaxFormMixin_Home by overiding parent class + define auto_id for generated fields
    def get(self, request, *args, **kwargs):
        print("BaseView Sales: GET request called. ")
        self.form_class = DeliveryPlanForm
        context = super(BaseView, self).get_context_data(**kwargs)
        context.update({
                    'deliveryPlan_Form': DeliveryPlanForm(auto_id='DeliveryPlanForm_%s'), 
                    'customerID_Form': CustomerIDForm(auto_id='CustomerIDForm_%s'),
                     })
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):   
        print("BaseView Sales: POST request called. ")

        # Decide validation form class
        if (request.POST.get('ajaxStatus') == 'addDeliveryNoteForm'):
            self.form_class = DeliveryPlanForm
        else:
            self.form_class = CustomerIDForm

        print('{}{}{}{}'.format("POST ajaxStatus: ", request.POST.get('ajaxStatus'), " $ Form Class: ", self.form_class ))

        form = self.get_form()
        if form.is_valid():
            return self.form_valid_sales(form)
        else:
            return self.form_invalid_sales(form)

# RefershUserToDoView -> TemplateView handles render_to_responce, which returns an HTTPResponse 
class RefreshDeliveryPlanView(AjaxFormMixin_Sales, TemplateView):
    template_name = 'sales/includes/objectList.html'

class RefreshCustomerIDView(AjaxFormMixin_Sales, TemplateView):
    template_name = 'sales/includes/searchCustomerID.html'

# EditUserToDoView must generate a tempalte with a form to pass object information to
class EditDeliveryPlanView(AjaxFormMixin_Sales, FormMixin, TemplateResponseMixin, View):
    form_class = DeliveryPlanForm
    success_url = reverse_lazy('home:index')
    template_name = 'sales/includes/editDeliveryPlanForm.html'

    # get data from database -> different from get_context_data as it does not return an HTTPResponse
    def get(self, request, *args, **kwargs):
        print("Sales EditDeliveryPlanView: GET request called. ")

        # Get author object and form instance and return from instance to view
        obj = get_object_or_404(DeliveryPlan, pk=self.kwargs['pk'])
        form = DeliveryPlanForm(instance=obj, auto_id='Edit_DeliveryPlanForm_%s')
        print(form)
        return self.render_to_response({'subForm': form})

    # Post data to database
    def post(self, request, *args, **kwargs):
        print("Sales EditDeliveryPlanView: POST request called. ")

        form = self.get_form()
        if form.is_valid():
            return self.form_valid_sales(form)
        else:
            return self.form_invalid_sales(form)

# EditUserToDoView must generate a tempalte with a form to pass object information to
class EditCustomerIDView(AjaxFormMixin_Sales, FormMixin, TemplateResponseMixin, View):
    form_class = CustomerIDForm
    success_url = reverse_lazy('home:index')
    template_name = 'sales/includes/editCustomerIDForm.html'

    # get data from database -> different from get_context_data as it does not return an HTTPResponse
    def get(self, request, *args, **kwargs):
        print("Sales EditCustomerIDView: GET request called. ")

        # Get author object and form instance and return from instance to view
        obj = get_object_or_404(CustomerID, pk=self.kwargs['pk'])
        form = CustomerIDForm(instance=obj, auto_id='Edit_DeliveryPlanForm_%s')
        print(form)
        return self.render_to_response({'subForm': form})

    # Post data to database
    def post(self, request, *args, **kwargs):
        print("Sales EditCustomerIDView: POST request called. ")

        form = self.get_form()
        if form.is_valid():
            return self.form_valid_sales(form)
        else:
            return self.form_invalid_sales(form)

# DeleteUserToDoView does not need to return a template. As AJAX, it just needs to post data to the database and return a Jsonresponse
class DeleteSalesView(View):

    # @method_decorator(ensure_csrf_cookie) -> Does not assist with AJAX requests
    def post(self, request, *args, **kwargs):
        print("production DeleteModel: POST request called to delete object. ")
        print('{}{}{}{}'.format("ajaxStatus: ", request.POST.get('ajaxStatus'), " pk: ", self.kwargs['pk']))
        return self.deleteObject(request.POST.get('ajaxStatus'), self.kwargs['pk'])

    def deleteObject(self, ajaxStatus, pk):
        print('{}{}'.format("ajaxStatus: ", ajaxStatus))
        try:
            if (ajaxStatus=="deliveredDeliveryPlanForm"):
                _ = get_object_or_404(DeliveryPlan, pk=pk)
                print('{}{}'.format("Delivery plan to updated: ", _))
                _.active = "Delivered"
                _.save()
                return JsonResponse('Delivery plan updated!', safe=False)

            elif (ajaxStatus=="deleteCustomerIDForm"):
                # Delete CustomerID and associated DeliveryPlans
                _ = get_object_or_404(CustomerID, pk=pk)
                print('{}{}'.format("Object to delete: ", _))
                
                # if the list is empty, delete the CustomerID only
                if not DeliveryPlan.objects.filter(customerID=_):
                    _.delete()
                    print('{}'.format("CustomerID deleted!"))
                    return JsonResponse('Customer deleted!', safe=False)
                else:
                    DeliveryPlan.objects.filter(customerID=_).delete()
                    _.delete()
                    print('{}'.format("Delivery plans deleted!"))
                    return JsonResponse('Delivery plan deleted!', safe=False)
                
            else:
                return JsonResponse({"message": 'Oops! Looks like something went wrong, contact your administrator!'})

        except:
            traceback.print_exc()
            return JsonResponse({"message": 'Oops! Looks like something went wrong, contact your administrator!'})


# # SearchDeliveryPlanView must generate a tempalte to pass initial result object to page through ajax, JS decides whether the object list should be handled as a general context or a search request
# class SearchDeliveryPlanView(AjaxFormMixin_Sales, TemplateView):
#     template_name = 'sales/includes/searchDeliveryPlan.html'

# SearchObjectView must generate a tempalte to pass context objects to page through ajax
class SearchCustomerIDView(AjaxFormMixin_Sales, TemplateView):
    template_name = 'sales/includes/searchCustomerID.html'

# Pagination view to handle general pagination requests and search requests
class HandleSalesPagination(AjaxFormMixin_Sales, ContextMixin, View):
        template_name = 'sales/includes/objectList.html'

        # A pagination request is made here
        def get(self, request, *args, **kwargs):
            print("Sales HandlePagination: GET request called. ")
            print('{}{}'.format("Sales HandlePagination: ajaxStatus -> ", request.GET.get('ajaxStatus')))
            print('{}{}'.format("Sales HandlePagination: searchObjectFieldText -> ", request.GET.get('searchObjectFieldText')))
            print('{}{}'.format("Sales HandlePagination: searchDeliveryPlanPage -> ", request.GET.get('searchDeliveryPlanPage')))

            # User searches for a DeliveryPlan
            searchText = self.request.GET.get('searchObjectFieldText')
            print('HandleSalesPagination:searchText -> {}'.format(searchText))
            
            # Call context data to make forms available after search
            context = super(HandleSalesPagination, self).get_context_data(**kwargs)

            try:
                if (request.GET.get('ajaxStatus') == "search_DeliveryPlans"):
                    print("HandleSalesPagination: -> request to search for a DeliveryPlan")
                    print('{}{}'.format("searchText for DeliveryPlan: ", searchText))
                    print('{}{}'.format("requestType: ", request.GET.get('requestType')))
                    print('{}{}'.format("searchDeliveryPlanPage: ", request.GET.get('searchDeliveryPlanPage')))
                    if (self.request.GET.get('requestType') == "customer" ) or (self.request.GET.get('radio') == "customer"):
                        print("HandleSalesPagination: -> request to search for a customer")
                        context.update({"paginated_Sales" : Paginator(DeliveryPlan.objects.filter(customerID__in=CustomerID.objects.filter(customerName__contains=searchText)).distinct(), 5).page(request.GET.get('searchDeliveryPlanPage'))})
                        return render(
                            request,
                            self.template_name,
                            context)
                    elif (self.request.GET.get('requestType') == "date to be delivered" ) or (self.request.GET.get('radio') == "date to be delivered"):
                        print("HandleSalesPagination: -> request to search for a date")
                        context.update({"paginated_Sales" : Paginator(DeliveryPlan.objects.filter(dateOfDelivery=datetime.strptime(searchText, "%Y-%m-%d").strftime("%Y-%m-%d")), 5).page(request.GET.get('searchDeliveryPlanPage'))})
                        return render(
                            request,
                            self.template_name,
                            context)

                    elif (self.request.GET.get('requestType') == "order placed on" ) or (self.request.GET.get('radio') == "order placed on"):
                        print("HandleSalesPagination: -> request to search for a date")
                        context.update({"paginated_Sales" : Paginator(DeliveryPlan.objects.filter(orderDate=datetime.strptime(searchText, "%Y-%m-%d").strftime("%Y-%m-%d")), 5).page(request.GET.get('searchDeliveryPlanPage'))})
                        return render(
                            request,
                            self.template_name,
                            context)

                    elif (self.request.GET.get('requestType') == "invoice number" ) or (self.request.GET.get('radio') == "invoice number"):
                        print("HandleSalesPagination: -> request to search for invoice number")
                        context.update({"paginated_Sales" : Paginator(DeliveryPlan.objects.filter(invoiceNumber__contains=searchText), 5).page(request.GET.get('searchDeliveryPlanPage'))})
                        return render(
                            request,
                            self.template_name,
                            context)

                    elif (self.request.GET.get('requestType') == "status" ) or (self.request.GET.get('radio') == "status"):
                        print("HandleSalesPagination: -> request to search for invoice number")
                        context.update({"paginated_Sales" : Paginator(DeliveryPlan.objects.filter(active=searchText), 5).page(request.GET.get('searchDeliveryPlanPage'))})
                        return render(
                            request,
                            self.template_name,
                            context)
                    else:
                        return JsonResponse({"message" : "Select a filter!"})
                
                elif (request.GET.get('ajaxStatus') == "search_EDIT_CustomerID"):
                    print("HandleSalesPagination: -> request to search for a CustomerID")
                    print('{}{}'.format("searchText for customerIDPage: ", searchText))
                    print('{}{}'.format("requestType: ", request.GET.get('requestType'))) 
                    print('{}{}'.format("customerIDPage: ", request.GET.get('customerIDPage'))) 
                    context.update({"searchCustomerID_results" : Paginator(CustomerID.objects.filter(customerName__contains=searchText).order_by('customerName'),5).page(request.GET.get('customerIDPage'))})
                    return render(
                            request,
                            'sales/includes/searchCustomerID.html',
                             context)

                elif (self.request.is_ajax() and (self.request.GET.get('customerIDPaginate'))):
                    print("HandleSalesPagination: -> request to paginate CustomerID search results")
                    print('{}{}'.format("searchText for customerIDPage: ", searchText))
                    print('{}{}'.format("requestType: ", request.GET.get('requestType')))

                    if searchText is None:
                        searchText = " "

                    context.update({"searchCustomerID_results" : Paginator(CustomerID.objects.filter(customerName__contains=searchText).order_by('customerName'),5).page(request.GET.get('customerIDPage'))})
                    return render(
                            request,
                            'sales/includes/searchCustomerID.html',
                             context)
                else:
                    return JsonResponse({"message" : "Select a filter!"})
                        
            except :
                traceback.print_exc()
                return JsonResponse({"errorMessage" : "Invalid search procedure! Contact the administrator!"})



