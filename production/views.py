from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView, TemplateResponseMixin, ContextMixin
from django.views.generic import FormView, View, ListView
from django.views.generic.edit import FormMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import JsonResponse
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProductionMeetingForm, ProductionNoteForm, RMShortageForm, MaintenanceIssueForm, ProductionPlanForm, RMReferenceForm
from .mixins import AjaxFormMixin_Production
from production.models import ProdMeeting, RMShortage, MaintenanceIssue, ProdNote, ProductionPlan, RMReference
import traceback


# RETURN A GENERIC TEMPLATE VIEW
class ProductionPageView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'production/home.html'

# Home view to redirect user
class BaseView(AjaxFormMixin_Production, FormMixin, TemplateResponseMixin, View):
    success_url = reverse_lazy('home:index')
    template_name  = 'home/home.html'

    # get request for home page -> return context from AjaxFormMixin_Home by overiding parent class + define auto_id for generated fields
    def get(self, request, *args, **kwargs):
        print("BaseView Production: GET request called. ")
        self.form_class = ProductionMeetingForm
        context = super(BaseView, self).get_context_data(**kwargs)
        context.update({
                    'productionMeeting_Form': ProductionMeetingForm(auto_id='ProductionMeetingForm_%s'),
                    'productionNote_Form': ProductionNoteForm(auto_id='ProductionNoteForm_%s'),
                    'rmShortage_Form': RMShortageForm(auto_id='rmShortage_Form_%s'), 
                    'maintenanceIssue_Form': MaintenanceIssueForm(auto_id='maintenanceIssue_Form_%s'),
                    'ProductionPlan_Form': ProductionPlanForm(auto_id='ProductionPlan_Form_%s'),
                    'RMReference_Form': RMReferenceForm(auto_id='RMReference_Form_%s'),
                     })
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):   
        print("BaseView Production: POST request called. ")

        # Decide validation form class
        if (request.POST.get('ajaxStatus') == 'addProductionNoteForm'):
            self.form_class = ProductionNoteForm
        elif (request.POST.get('ajaxStatus') == 'addRMSHortageForm'):
            self.form_class = RMShortageForm
        elif (request.POST.get('ajaxStatus') == 'addMaintenanceIssueForm'):
            self.form_class = MaintenanceIssueForm
        elif (request.POST.get('ajaxStatus') == 'addProductionPlanForm'):
            self.form_class = ProductionPlanForm
        elif (request.POST.get('ajaxStatus') == 'addRM_Reference'):
            self.form_class = RMReferenceForm
        else:
            self.form_class = ProductionMeetingForm

        print('{}{}{}{}'.format("POST ajaxStatus: ", request.POST.get('ajaxStatus'), " $ Form Class: ", self.form_class ))

        form = self.get_form()
        if form.is_valid():
            return self.form_valid_production(form)
        else:
            return self.form_invalid_production(form)

# RefershUserToDoView -> TemplateView handles render_to_responce, which returns an HTTPResponse 
class RefreshProductionView(AjaxFormMixin_Production, TemplateView):
    template_name = 'production/includes/objectList.html'

# EditUserToDoView must generate a tempalte with a form to pass object information to
class EditProductionMeetingView(AjaxFormMixin_Production, FormMixin, TemplateResponseMixin, View):
    form_class = ProductionMeetingForm
    success_url = reverse_lazy('home:index')
    template_name = 'production/includes/editProductionMeetingForm.html'

    # get data from database -> different from get_context_data as it does not return an HTTPResponse
    def get(self, request, *args, **kwargs):
        print("Production EditUserToDoView: GET request called. ")

        # Get author object and form instance and return from instance to view
        obj = get_object_or_404(ProdMeeting, pk=self.kwargs['pk'])
        form = ProductionMeetingForm(instance=obj, auto_id='Edit_ProductionMeetingForm_%s')
        print(form)
        return self.render_to_response({'subForm': form})

    # Post data to database
    def post(self, request, *args, **kwargs):
        print("Production EditProductionMeetingView: POST request called. ")

        form = self.get_form()
        if form.is_valid():
            return self.form_valid_production(form)
        else:
            return self.form_invalid_production(form)

# EditUserToDoView must generate a tempalte with a form to pass object information to
class EditProductionNoteView(AjaxFormMixin_Production, FormMixin, TemplateResponseMixin, View):
    form_class = ProductionNoteForm
    success_url = reverse_lazy('home:index')
    template_name = 'production/includes/editProductionNoteForm.html'

    # get data from database -> different from get_context_data as it does not return an HTTPResponse
    def get(self, request, *args, **kwargs):
        print("Production EditProductionNoteView: GET request called. ")
        print('{}{}'.format("Production EditProductionNoteView: pk -> ", self.kwargs['pk']))
        
        # Get author object and form instance and return from instance to view
        obj = get_object_or_404(ProdNote, pk=self.kwargs['pk'])
        form = ProductionNoteForm(instance=obj, auto_id='Edit_ProductionNoteForm_%s')
        # print('{}{}{}{}'.format("pk: ", self.kwargs['pk']),"subform: ", form)

        return self.render_to_response({'subForm': form})

    # Post data to database
    def post(self, request, *args, **kwargs):
        print("Production EditProductionMeetingView: POST request called. ")

        form = self.get_form()
        if form.is_valid():
            return self.form_valid_production(form)
        else:
            return self.form_invalid_production(form)
# EditUserToDoView must generate a tempalte with a form to pass object information to
class EditRMReference(AjaxFormMixin_Production, FormMixin, TemplateResponseMixin, View):
    form_class = RMReferenceForm
    success_url = reverse_lazy('home:index')
    template_name = 'production/includes/editRawMaterial.html'

    # get data from database -> different from get_context_data as it does not return an HTTPResponse
    def get(self, request, *args, **kwargs):
        print("Production EditRMReference: GET request called. ")
        print('{}{}'.format("Production EditRMReference: pk -> ", self.kwargs['pk']))
        
        # Get author object and form instance and return from instance to view
        obj = get_object_or_404(RMReference, pk=self.kwargs['pk'])
        form = RMReferenceForm(instance=obj, auto_id='Edit_rmShortage_Form_%s')
        # print('{}{}{}{}'.format("pk: ", self.kwargs['pk']),"subform: ", form)

        return self.render_to_response({'subForm': form})

    # Post data to database
    def post(self, request, *args, **kwargs):
        print("Production EditProductionMeetingView: POST request called. ")

        form = self.get_form()
        if form.is_valid():
            return self.form_valid_production(form)
        else:
            return self.form_invalid_production(form)

# EditUserToDoView must generate a tempalte with a form to pass object information to
class EditRMShortageView(AjaxFormMixin_Production, FormMixin, TemplateResponseMixin, View):
    form_class = RMShortageForm
    success_url = reverse_lazy('home:index')
    template_name = 'production/includes/editRMShortage.html'

    # get data from database -> different from get_context_data as it does not return an HTTPResponse
    def get(self, request, *args, **kwargs):
        print("Production EditRMShortageView: GET request called. ")
        print('{}{}'.format("Production EditRMShortageView: pk -> ", self.kwargs['pk']))
        
        # Get author object and form instance and return from instance to view
        obj = get_object_or_404(RMShortage, pk=self.kwargs['pk'])
        form = RMShortageForm(instance=obj, auto_id='Edit_rmShortage_Form_%s')
        # print('{}{}{}{}'.format("pk: ", self.kwargs['pk']),"subform: ", form)

        return self.render_to_response({'subForm': form})

    # Post data to database
    def post(self, request, *args, **kwargs):
        print("Production EditProductionMeetingView: POST request called. ")

        form = self.get_form()
        if form.is_valid():
            return self.form_valid_production(form)
        else:
            return self.form_invalid_production(form)

# EditUserToDoView must generate a tempalte with a form to pass object information to
class EditMaintenanceIssueView(AjaxFormMixin_Production, FormMixin, TemplateResponseMixin, View):
    form_class = MaintenanceIssueForm
    success_url = reverse_lazy('home:index')
    template_name = 'production/includes/editMaintenanceIssue.html'

    # get data from database -> different from get_context_data as it does not return an HTTPResponse
    def get(self, request, *args, **kwargs):
        print("Production EditMaintenanceIssueView: GET request called. ")
        print('{}{}'.format("Production EditMaintenanceIssueView: pk -> ", self.kwargs['pk']))
        
        # Get author object and form instance and return from instance to view
        obj = get_object_or_404(MaintenanceIssue, pk=self.kwargs['pk'])
        form = MaintenanceIssueForm(instance=obj, auto_id='Edit_maintenanceIssue_Form_%s')
        # print('{}{}{}{}'.format("pk: ", self.kwargs['pk']),"subform: ", form)

        return self.render_to_response({'subForm': form})

    # Post data to database
    def post(self, request, *args, **kwargs):
        print("Production EditProductionMeetingView: POST request called. ")

        form = self.get_form()
        if form.is_valid():
            return self.form_valid_production(form)
        else:
            return self.form_invalid_production(form)

# EditUserToDoView must generate a tempalte with a form to pass object information to
class EditProductionPlanView(AjaxFormMixin_Production, FormMixin, TemplateResponseMixin, View):
    form_class = ProductionPlanForm
    success_url = reverse_lazy('home:index')
    template_name = 'production/includes/editProductionPlanForm.html'

    # get data from database -> different from get_context_data as it does not return an HTTPResponse
    def get(self, request, *args, **kwargs):
        print("Production EditProductionPlanView: GET request called. ")
        print('{}{}'.format("Production EditProductionPlanView: pk -> ", self.kwargs['pk']))
        
        # Get author object and form instance and return from instance to view
        obj = get_object_or_404(ProductionPlan, pk=self.kwargs['pk'])
        form = ProductionPlanForm(instance=obj, auto_id='Edit_ProductionPlan_Form_%s')
        # print('{}{}{}{}'.format("pk: ", self.kwargs['pk']),"subform: ", form)

        return self.render_to_response({'subForm': form})

    # Post data to database
    def post(self, request, *args, **kwargs):
        print("Production EditProductionMeetingView: POST request called. ")

        form = self.get_form()
        if form.is_valid():
            return self.form_valid_production(form)
        else:
            return self.form_invalid_production(form)
# DeleteUserToDoView does not need to return a template. As AJAX, it just needs to post data to the database and return a Jsonresponse
class DeleteModelView(View):

    # @method_decorator(ensure_csrf_cookie) -> Does not assist with AJAX requests
    def post(self, request, *args, **kwargs):
        print("production DeleteModel: POST request called to delete object. ")
        print('{}{}{}{}'.format("ajaxStatus: ", request.POST.get('ajaxStatus'), " pk: ", self.kwargs['pk']))
        return self.deleteObject(request.POST.get('ajaxStatus'), self.kwargs['pk'])
    

    def deleteObject(self, ajaxStatus, pk):
        print('{}{}'.format("ajaxStatus: ", ajaxStatus))
        try:
            if (ajaxStatus=="deleteProductionMeetingForm"):
                _ = get_object_or_404(ProdMeeting, pk=pk)
                print('{}{}'.format("Object to delete: ", _))
                _.delete()
                return JsonResponse({"message": 'Production meeting deleted succesfully!'})

            elif (ajaxStatus=="deleteProductionNote"):
                _ = get_object_or_404(ProdNote, pk=pk)
                print('{}{}'.format("Object to delete: ", _))
                _.delete()
                return JsonResponse({"message": 'Production note deleted succesfully!'})

            elif (ajaxStatus=="deleteRMShortageForm"):
                _ = get_object_or_404(RMShortage, pk=pk)
                print('{}{}'.format("Object to delete: ", _))
                _.delete()
                return JsonResponse({"message": 'Raw material shortage deleted succesfully!'})

            elif (ajaxStatus=="deleteRawMaterial"):
                # Delete the raw material and shortages involved
                _ = get_object_or_404(RMReference, pk=pk)
                print('{}{}'.format("Object to delete: ", _))

                # if the list is empty, delete the CustomerID only
                if not RMShortage.objects.filter(rmShortage=_):
                    _.delete()
                    print('{}'.format("Raw material deleted!"))
                    return JsonResponse({ "message": 'Raw material deleted!'})
                else:
                    RMShortage.objects.filter(rmShortage=_).delete()
                    _.delete()
                    print('{}'.format("Raw material and shortages!"))
                    return JsonResponse({ "message": 'Raw material and shortages deleted!'})

            elif (ajaxStatus=="deleteMaintenanceIssueForm"):
                _ = get_object_or_404(MaintenanceIssue, pk=pk)
                print('{}{}'.format("Object to delete: ", _))
                _.delete()
                return JsonResponse({"message": 'Maintenance form deleted succesfully!'})
            
            elif (ajaxStatus=="deleteProductionPlanForm"):
                _ = get_object_or_404(ProductionPlan, pk=pk)
                print('{}{}'.format("Object to delete: ", _))
                _.delete()
                return JsonResponse({"message": 'Production plan deleted succesfully!'})

            else:
                return JsonResponse({"message": 'Oops! Looks like something went wrong, contact your administrator!'})

        except:
            traceback.print_exc()
            return JsonResponse({"message": 'Oops! Looks like something went wrong, contact your administrator!'})

# # SearchObjectView must generate a tempalte to pass context objects to
# class SearchProductionView(AjaxFormMixin_Production, TemplateView):
#     template_name = 'production/includes/objectList.html'

# Pagination view to handle general pagination requests and search requests
class HandleProductionPagination(AjaxFormMixin_Production, ContextMixin, View):
        template_name = 'production/includes/objectList.html'

        # A pagination request is made here
        def get(self, request, *args, **kwargs):
            print("Production HandlePagination: GET request called. ")
            

            # Call context data to make forms available after search
            context = super(HandleProductionPagination, self).get_context_data(**kwargs)

            try:
                print('{}{}'.format("HandleProductionPagination: ajaxStatus -> ", request.GET.get('ajaxStatus')))
                print('{}{}'.format("HandleProductionPagination: searchObjectFieldText -> ", request.GET.get('searchObjectFieldText')))
                print('{}{}'.format("HandleProductionPagination: searchProductionPage -> ", request.GET.get('searchProductionPage')))
                print('{}{}'.format("HandleProductionPagination: radio -> ", request.GET.get('radio')))
                # User searches for something
                searchText = request.GET.get('searchObjectFieldText')

                if (request.GET.get('ajaxStatus') == "search_ProductionMeetings"):
                    print("HandleProductionPagination -> request to search Production Meetings")
                    searchText = request.GET.get('searchObjectFieldText')
                    print('HandleProductionPagination:searchText -> {}'.format(request.GET.get('searchObjectFieldText')))
                    if (request.GET.get('requestType') == "subject of meeting" ) or (request.GET.get('radio') == "subject of meeting"):
                        context.update({"paginated_Production" : Paginator(ProdMeeting.objects.filter(subject__contains=searchText), 5).page(request.GET.get('searchProductionPage'))})
                        return render(
                            request,
                            self.template_name,
                            context)
                    else:
                        # Modifty this
                        return JsonResponse({"message" : "Select a filter!"})

                # Since ProdNote can be in many UserToDo's, perform query to return relevant UserToDo objects
                elif (request.GET.get('ajaxStatus') == "search_ProductionNotes"):
                    print("AjaxFormMixin_Production:handleAjax called -> request to search Production Notes")
                    searchText = self.request.GET.get('searchObjectFieldText')
                    print('AjaxFormMixin_Production:searchText -> {}'.format(request.GET.get('searchObjectFieldText')))
                    if (request.GET.get('requestType') == "production note" ) or (self.request.GET.get('radio') == "production note"):
                        context.update({"paginated_Production" : Paginator(ProdMeeting.objects.filter(prodnote__in=ProdNote.objects.filter(prodNote__contains=searchText)).distinct(), 5).page(request.GET.get('searchProductionPage'))})
                        return render(
                            request,
                            self.template_name,
                            context)

                    else:
                        return JsonResponse({"message" : "Select a filter!"})

                # Since RMShortage can be in many UserToDo's, perform query to return relevant UserToDo objects
                elif (request.GET.get('ajaxStatus') == "search_RMShortages"):
                    print("AjaxFormMixin_Production:handleAjax called -> request to search Raw Material Shortage")
                    searchText = self.request.GET.get('searchObjectFieldText')
                    print('AjaxFormMixin_Production:searchText -> {}'.format(request.GET.get('searchObjectFieldText')))
                    r = RMReference.objects.filter(rmDescription__contains=searchText)
                    if (request.GET.get('requestType') == "name of raw material" ) or (request.GET.get('radio') == "name of raw material"):
                        context.update({"paginated_Production" : Paginator(ProdMeeting.objects.filter(rmshortage__in=RMShortage.objects.filter(rmShortage=r)).distinct(), 5).page(request.GET.get('searchProductionPage'))})
                        return render(
                            request,
                            self.template_name,
                            context)
                    elif (request.GET.get('requestType') == "level of shortage" ) or (request.GET.get('radio') == "level of shortage"):
            
                        try:
                            context.update({"paginated_Production" : Paginator(ProdMeeting.objects.filter(rmshortage__in=RMShortage.objects.filter(rmLevel__contains=int(searchText))).distinct(), 5).page(request.GET.get('searchProductionPage'))})
                            return render(
                                request,
                                self.template_name,
                                context)
                        except:
                            return JsonResponse({"message" : "Enter a number!"})

                    elif (request.GET.get('requestType') == "status of shortage" ) or (request.GET.get('radio') == "status of shortage"):
                        context.update({"paginated_Production" : Paginator(ProdMeeting.objects.filter(rmshortage__in=RMShortage.objects.filter(rmStatus__contains=searchText)).distinct(), 5).page(request.GET.get('searchProductionPage'))})
                        return render(
                            request,
                            self.template_name,
                            context)                   
                    else:
                        return JsonResponse({"message" : "Select a filter!"})

                # Since MaintenanceIssue can be in many ProdMeeting's, perform query to return relevant ProdMeeting objects
                elif (request.GET.get('ajaxStatus') == "search_MaintenanceIssues"):
                    print("AjaxFormMixin_Production:handleAjax called -> request to search Maintenance Issue")
                    searchText = self.request.GET.get('searchObjectFieldText')
                    print('AjaxFormMixin_Production:searchText -> {}'.format(request.GET.get('searchObjectFieldText')))
                    if request.GET.get('radio') == "type of maintenance issue":
                        context.update({"paginated_Production" : Paginator(ProdMeeting.objects.filter(maintenanceissue__in=MaintenanceIssue.objects.filter(maintenanceType__contains=searchText)).distinct(), 5).page(request.GET.get('searchProductionPage'))})
                        return render(
                            request,
                            self.template_name,
                            context)
                    elif request.GET.get('radio') == "subject":
                        context.update({"paginated_Production" : Paginator(ProdMeeting.objects.filter(maintenanceissue__in=MaintenanceIssue.objects.filter(subject__contains=searchText)).distinct(), 5).page(request.GET.get('searchProductionPage'))})
                        return render(
                            request,
                            self.template_name,
                            context)
                    elif request.GET.get('radio') == "status":
                        context.update({"paginated_Production" : Paginator(ProdMeeting.objects.filter(maintenanceissue__in=MaintenanceIssue.objects.filter(active__contains=searchText)).distinct(), 5).page(request.GET.get('searchProductionPage'))})
                        return render(
                            request,
                            self.template_name,
                            context)
                    elif request.GET.get('radio') == "action required":
                        context.update({"paginated_Production" : Paginator(ProdMeeting.objects.filter(maintenanceissue__in=MaintenanceIssue.objects.filter(note__contains=searchText)).distinct(), 5).page(request.GET.get('searchProductionPage'))})
                        return render(
                            request,
                            self.template_name,
                            context)
                    else:
                        return JsonResponse({"message" : "Select a filter!"})

                elif (request.GET.get('ajaxStatus') == "search_EDIT_RawMaterialPaginate"):
                    print("HandleQualityPagination: -> request to search for a raw material")
                    print('{}{}'.format("searchText for rmPRoject: ", searchText))
                    print('{}{}'.format("Search Page: ", request.GET.get('searchRawMaterialsPage')))
                    print('{}{}'.format("requestType: ", request.GET.get('requestType'))) 
                    print('{}{}'.format("rdProject: ", request.GET.get('rdProject'))) 
                    context.update({"searchRawMaterial_results" : Paginator(RMReference.objects.filter(rmCode__contains=searchText),5).page(request.GET.get('searchRawMaterialsPage'))})
                    return render(
                            request,
                            'production/includes/searchRawMaterials.html',
                             context)

                elif (self.request.is_ajax() and (self.request.GET.get('RawMaterialPaginate'))):
                    print("HandleQualityPagination: -> request to paginate raw material search results")
                    print('{}{}'.format("searchText for rdProject page: ", searchText))
                    print('{}{}'.format("requestType: ", request.GET.get('requestType')))

                    if searchText is None:
                        searchText = " "

                    context.update({"searchRawMaterial_results" : Paginator(RMReference.objects.filter(rmCode__contains=searchText),5).page(request.GET.get('searchRawMaterialsPage'))})
                    
                    return render(
                            request,
                            'production/includes/searchRawMaterials.html',
                             context)

                else: 
                    return JsonResponse({"message" : "Select a filter!"})

            except :
                traceback.print_exc()
                return JsonResponse({"errorMessage" : "Invalid search procedure! Contact the administrator!"})


