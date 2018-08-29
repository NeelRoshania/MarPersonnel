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
from quality.mixins import AjaxFormMixin_Quality
from quality.forms import PaintInfoForm, BatchAdjustmentForm, RDProjectForm, ProductTypeForm, PremixInfoForm, BatchInfoForm, BatchAdjustmentForm
from quality.models import PaintInfo, RDProject, FinishingAdjustment, ProductType
from sales.models import DeliveryPlan, CustomerID
from sales.forms import DeliveryPlanForm, CustomerIDForm
import traceback

# Create your views here.

# This view is called whenever an object needs to be retrieved or inserted. Not redirect on home page request! 
class BaseView(AjaxFormMixin_Quality, FormMixin, TemplateResponseMixin, View):
	success_url = reverse_lazy('home:index')
	template_name  = 'home/home.html'

	# get request for home page -> return context from AjaxFormMixin_Home by overiding parent class + define auto_id for generated fields
	def get(self, request, *args, **kwargs):
	    print("BaseView Quality: GET request called. ")
	    self.form_class = DeliveryPlanForm
	    context = super(BaseView, self).get_context_data(**kwargs)
	    context.update({
	    			'productType_Form': ProductTypeForm(auto_id='ProductTypeForm_%s'),
	                'paintInfo_Form': PaintInfoForm(auto_id='PaintInfoForm_%s'),
	                'batchAdjustment_Form': BatchAdjustmentForm(auto_id='BatchAdjustmentForm_%s'),
	                'RDProject_Form' : RDProjectForm(auto_id='RDProjectForm_%s'),
	                 })
	    return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):   
		print("BaseView Quality: POST request called. ")

		# Decide validation form class
		if (request.POST.get('ajaxStatus') == 'addNewBatchForm'):
		    self.form_class = PaintInfoForm
		elif (request.POST.get('ajaxStatus') == 'addRDProject'):
			self.form_class = RDProjectForm
		elif (request.POST.get('ajaxStatus') == 'addProductTypeForm'):
			self.form_class = ProductTypeForm
		else:
			self.form_class = BatchAdjustmentForm

		print('{}{}{}{}'.format("POST ajaxStatus: ", request.POST.get('ajaxStatus'), " $ Form Class: ", self.form_class ))

		form = self.get_form()
		if form.is_valid():
		    return self.form_valid_quality(form)
		else:
		    return self.form_invalid_quality(form)

# RefershUserToDoView -> TemplateView handles render_to_responce, which returns an HTTPResponse 
class RefreshQualityView(AjaxFormMixin_Quality, TemplateView):
    template_name = 'quality/includes/objectList.html'

# class RefreshCustomerIDView(AjaxFormMixin_Quality, TemplateView):
#     template_name = 'sales/includes/searchCustomerID.html'

# EditUserToDoView must generate a tempalte with a form to pass object information to
class EditPaintInfo(AjaxFormMixin_Quality, FormMixin, TemplateResponseMixin, View):
    form_class = PaintInfoForm
    success_url = reverse_lazy('home:index')
    template_name = 'quality/includes/editPremixInfo.html'

    # get data from database -> different from get_context_data as it does not return an HTTPResponse
    def get(self, request, *args, **kwargs):
        print("Quality EditPaintInfo: GET request called. ")
        print('ajaxStatus: {}'.format(request.GET.get('ajaxStatus')))

        # Change template name depending on ajaxStatus
        if (request.GET.get('ajaxStatus') == 'editBatchInformation'):
        	self.template_name = 'quality/includes/editBatchInfo.html'
        	self.form_class = BatchInfoForm
        	obj = get_object_or_404(PaintInfo, pk=self.kwargs['pk'])
        	form = BatchInfoForm(instance=obj, auto_id='Edit_BatchInfoForm_%s')
        elif (request.GET.get('ajaxStatus') == 'editFinishingAdjustments'):
        	self.template_name = 'quality/includes/editFinishingAdjustments.html'
        	self.form_class = BatchAdjustmentForm
        	obj = get_object_or_404(FinishingAdjustment, pk=self.kwargs['pk'])
        	form = BatchAdjustmentForm(instance=obj, auto_id='Edit_BatchAdjustmentForm_%s')
        else:
        	self.template_name = 'quality/includes/editPremixInfo.html'
        	self.form_class = PremixInfoForm
        	obj = get_object_or_404(PaintInfo, pk=self.kwargs['pk'])
        	form = PremixInfoForm(instance=obj, auto_id='Edit_PaintInfoForm_%s') 

        # print(form)
        return self.render_to_response({'subForm': form})

    # Post data to database
    def post(self, request, *args, **kwargs):
        print("Quality EditPaintInfo: POST request called. ")

        # Change template name depending on ajaxStatus
        if (request.POST.get('ajaxStatus') == 'editBatchInformation'):
        	self.template_name = 'quality/includes/editBatchInfo.html'
        	self.form_class = BatchInfoForm
        elif (request.POST.get('ajaxStatus') == 'editFinishingAdjustments'):
        	self.template_name = 'quality/includes/editFinishingAdjustments.html'
        	self.form_class = BatchAdjustmentForm
        else:
        	self.template_name = 'quality/includes/editPremixInfo.html'
        	self.form_class = PremixInfoForm
        
        form = self.get_form()
        print('form_class: {}\n\nform instance: {}'.format(self.form_class, form))

        if form.is_valid():
            return self.form_valid_quality(form)
        else:
            return self.form_invalid_quality(form)

# EditUserToDoView must generate a tempalte with a form to pass object information to
class EditRDProjectView(AjaxFormMixin_Quality, FormMixin, TemplateResponseMixin, View):
    form_class = RDProjectForm
    success_url = reverse_lazy('home:index')
    template_name = 'quality/includes/editRDProject.html'

    # get data from database -> different from get_context_data as it does not return an HTTPResponse
    def get(self, request, *args, **kwargs):
        print("Quality EditRDProjectView: GET request called. ")

        # Get author object and form instance and return from instance to view
        obj = get_object_or_404(RDProject, pk=self.kwargs['pk'])
        form = RDProjectForm(instance=obj, auto_id='Edit_RDProject_%s')
        print(form)
        return self.render_to_response({'subForm': form})

    # Post data to database
    def post(self, request, *args, **kwargs):
        print("Quality EditRDProjectView: POST request called. ")

        form = self.get_form()
        if form.is_valid():
            return self.form_valid_quality(form)
        else:
            return self.form_invalid_quality(form)

# EditUserToDoView must generate a tempalte with a form to pass object information to
class EditBatchProductView(AjaxFormMixin_Quality, FormMixin, TemplateResponseMixin, View):
    form_class = ProductTypeForm
    success_url = reverse_lazy('home:index')
    template_name = 'quality/includes/editBatchProduct.html'

    # get data from database -> different from get_context_data as it does not return an HTTPResponse
    def get(self, request, *args, **kwargs):
        print("Quality EditBatchProductView: GET request called. ")

        # Get author object and form instance and return from instance to view
        obj = get_object_or_404(ProductType, pk=self.kwargs['pk'])
        form = ProductTypeForm(instance=obj, auto_id='Edit_ProductType_%s')
        print(form)
        return self.render_to_response({'subForm': form})

    # Post data to database
    def post(self, request, *args, **kwargs):
        print("Quality EditBatchProductView: POST request called. ")

        form = self.get_form()
        if form.is_valid():
            return self.form_valid_quality(form)
        else:
            return self.form_invalid_quality(form)

# DeleteUserToDoView does not need to return a template. As AJAX, it just needs to post data to the database and return a Jsonresponse
class DeleteQualityView(View):

    # @method_decorator(ensure_csrf_cookie) -> Does not assist with AJAX requests
    def post(self, request, *args, **kwargs):
        print("production DeleteModel: POST request called to delete object. ")
        print('{}{}{}{}'.format("ajaxStatus: ", request.POST.get('ajaxStatus'), " pk: ", self.kwargs['pk']))
        return self.deleteObject(request.POST.get('ajaxStatus'), self.kwargs['pk'], request)

    def deleteObject(self, ajaxStatus, pk, request):
        try:
            if (ajaxStatus=="updateQualityPlan"):
                _ = get_object_or_404(PaintInfo, pk=pk)
                print('{}{}'.format("PaintInfo to be updated: ", _))
                _.active = "Completed"
                _.passedBy.add(User.objects.get(id=request.user.id))
                _.save()
                return JsonResponse({"message":'Batch card updated!'})

            elif (ajaxStatus=="deleteQualityPlan"):
                _ = get_object_or_404(PaintInfo, pk=pk)
                print('{}{}'.format("Paint Info to be deleted: ", _))
                _.delete()
                return JsonResponse({"message":'Batch card deleted!'})

            elif (ajaxStatus=="deleteRDProjectForm"):
                _ = get_object_or_404(RDProject, pk=pk)
                print('{}{}'.format("Object to delete: ", _))

                # if the list is empty, delete the CustomerID only
                if not PaintInfo.objects.filter(rdProject=_):
                    _.delete()
                    print('{}'.format("R&D project deleted!"))
                    return JsonResponse({"message":'Lab project deleted!'})
                else:
                    PaintInfo.objects.filter(rdProject=_).delete()
                    _.delete()
                    print('{}'.format("R&D project deleted!"))
                    return JsonResponse({"message":'Lab project deleted!'})

            elif (ajaxStatus=="deleteBatchProduct"):
                _ = get_object_or_404(ProductType, pk=pk)
                print('{}{}'.format("Object to delete: ", _))

                # if the list is empty, delete the CustomerID only
                if not PaintInfo.objects.filter(productType=_):
                    _.delete()
                    print('{}'.format("ProductType deleted!"))
                    return JsonResponse({ "message": 'Batch Product deleted!'})
                else:
                    PaintInfo.objects.filter(productType=_).delete()
                    _.delete()
                    print('{}'.format("ProductType deleted!"))
                    return JsonResponse({ "message": 'Batch Product deleted!'})

            else:
                return JsonResponse({"message": 'Oops! Looks like something went wrong, contact your administrator!'})

        except:
            traceback.print_exc()
            return JsonResponse({"message": 'Oops! Looks like something went wrong, contact your administrator!'})


# # # SearchDeliveryPlanView must generate a tempalte to pass initial result object to page through ajax, JS decides whether the object list should be handled as a general context or a search request
# # class SearchDeliveryPlanView(AjaxFormMixin_Quality, TemplateView):
# #     template_name = 'sales/includes/searchDeliveryPlan.html'

# # SearchObjectView must generate a tempalte to pass context objects to page through ajax
# class SearchCustomerIDView(AjaxFormMixin_Quality, TemplateView):
#     template_name = 'sales/includes/searchCustomerID.html'

# Pagination view to handle general pagination requests and search requests
class HandleQualityPagination(AjaxFormMixin_Quality, ContextMixin, View):
        template_name = 'quality/includes/objectList.html'

        # A pagination request is made here
        def get(self, request, *args, **kwargs):
            print("quality HandlePagination: GET request called. ")
            print('{}{}'.format("quality HandlePagination: ajaxStatus -> ", request.GET.get('ajaxStatus')))
            print('{}{}'.format("quality HandlePagination: searchObjectFieldText -> ", request.GET.get('searchObjectFieldText')))
            print('{}{}'.format("quality HandlePagination: searchDeliveryPlanPage -> ", request.GET.get('searchDeliveryPlanPage')))

            # User searches for a DeliveryPlan
            searchText = self.request.GET.get('searchObjectFieldText')
            print('HandleQualityPagination:searchText -> {}'.format(searchText))
            
            # Call context data to make forms available after search
            context = {}

            try:
                if (request.GET.get('ajaxStatus') == "search_QualityPlans"):
                    print("HandleQualityPagination: -> request to search for a QualityPlan")
                    print('{}{}'.format("searchText for QualityPlan: ", searchText))
                    print('{}{}'.format("requestType: ", request.GET.get('requestType')))
                    if (self.request.GET.get('requestType') == "status of batch" ) or (self.request.GET.get('radio') == "status of batch"):
                        print("HandleQualityPagination: -> request to search for status of batch")
                        context.update({"paginated_Quality" : Paginator(PaintInfo.objects.filter(active__contains=searchText).distinct(), 5).page(request.GET.get('searchqualityListPage'))})
                        return render(
                            request,
                            self.template_name,
                            context)
                    elif (self.request.GET.get('requestType') == "name of product" ) or (self.request.GET.get('radio') == "name of product"):
                        print("HandleQualityPagination: -> request to search for batch card by product type")
                        context.update({"paginated_Quality" : Paginator(PaintInfo.objects.filter(productType__in=ProductType.objects.filter(productDescription__contains=searchText)), 5).page(request.GET.get('searchqualityListPage'))})
                        return render(
                            request,
                            self.template_name,
                            context)
                    elif (self.request.GET.get('requestType') == "productCode" ) or (self.request.GET.get('radio') == "productCode"):
                        print("HandleQualityPagination: -> request to search for batch card by product code")
                        context.update({"paginated_Quality" : Paginator(PaintInfo.objects.filter(productType__in=ProductType.objects.filter(productCode__contains=searchText)), 5).page(request.GET.get('searchqualityListPage'))})
                        return render(
                            request,
                            self.template_name,
                            context)
                    elif (self.request.GET.get('requestType') == "batchNumber" ) or (self.request.GET.get('radio') == "batchNumber"):
                        print("HandleQualityPagination: -> request to search for batch card by product code")
                        context.update({"paginated_Quality" : Paginator(PaintInfo.objects.filter(batchNumber__contains=searchText), 5).page(request.GET.get('searchqualityListPage'))})
                        return render(
                            request,
                            self.template_name,
                            context)

                    elif (self.request.GET.get('requestType') == "rdProject" ) or (self.request.GET.get('radio') == "rdProject"):
                        print("HandleQualityPagination: -> request to search for rd project")
                        context.update({"paginated_Quality" : Paginator(PaintInfo.objects.filter(rdProject__in=RDProject.objects.filter(customer__in=CustomerID.objects.filter(customerName__contains=searchText).distinct())).distinct(), 5).page(request.GET.get('searchqualityListPage'))})
                        return render(
                            request,
                            self.template_name,
                            context)

                    else:
                        return JsonResponse({"message" : "Select a filter!"})
                    
                elif (request.GET.get('ajaxStatus') == "search_EDIT_QualityProject"):
                    print("HandleQualityPagination: -> request to search for a Quality Project")
                    print('{}{}'.format("searchText for rdProject: ", searchText))
                    print('{}{}'.format("requestType: ", request.GET.get('requestType'))) 
                    print('{}{}'.format("rdProject: ", request.GET.get('rdProject'))) 
                    context.update({"searchRDProjects_results" : Paginator(RDProject.objects.filter(customer__in=CustomerID.objects.filter(customerName__contains=searchText).distinct()),5).page(request.GET.get('rdProject'))})
                    return render(
                            request,
                            'quality/includes/searchRDProjects.html',
                             context)

                elif (self.request.is_ajax() and (self.request.GET.get('RDProjectPaginate'))):
                    print("HandleQualityPagination: -> request to paginate R&DProject search results")
                    print('{}{}'.format("searchText for rdProject page: ", searchText))
                    print('{}{}'.format("requestType: ", request.GET.get('requestType')))

                    if searchText is None:
                        searchText = " "

                    context.update({"searchRDProjects_results" : Paginator(RDProject.objects.filter(customer__in=CustomerID.objects.filter(customerName__contains=searchText).distinct()),5).page(request.GET.get('rdProject'))})
                    
                    return render(
                            request,
                            'quality/includes/searchRDProjects.html',
                             context)

                elif (request.GET.get('ajaxStatus') == "search_EDIT_BatchProductPaginate"):
                    print("HandleQualityPagination: -> request to search for a batch product")
                    print('{}{}'.format("searchText for batch product: ", searchText))
                    print('{}{}'.format("requestType: ", request.GET.get('requestType')))
                    context.update({"searchBatchProduct_results" : Paginator(ProductType.objects.filter(productDescription__contains=searchText).order_by('productDescription'),5).page(request.GET.get('searchBatchProductListPage'))})
                    return render(
                            request,
                            'quality/includes/searchBatchProducts.html',
                             context)

                elif (self.request.is_ajax() and (self.request.GET.get('batchProductPaginate'))):
                    print("HandleQualityPagination: -> request to paginate batch product search results")
                    print('{}{}'.format("searchText for searchBatchProductListPage page: ", searchText))
                    print('{}{}'.format("requestType: ", request.GET.get('requestType')))

                    if searchText is None:
                        searchText = " "
                    context.update({"searchBatchProduct_results" : Paginator(ProductType.objects.filter(productDescription__contains=searchText).order_by('productDescription'),5).page(request.GET.get('searchBatchProductListPage'))})
                    
                    return render(
                            request,
                            'quality/includes/searchBatchProducts.html',
                             context)

                else:
                    return JsonResponse({"message" : "Select a filter!"})

            except :
                traceback.print_exc()
                return JsonResponse({"errorMessage" : "Invalid search procedure! Contact the administrator!"})




