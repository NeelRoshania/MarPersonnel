from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from quality.forms import PaintInfoForm, RDProjectForm, ProductTypeForm, BatchAdjustmentForm, PremixInfoForm
from quality.models import RDProject, ProductType, PaintInfo, FinishingAdjustment

class AjaxFormMixin_Quality(object):

    # Update the object if form is in-valid
    def form_invalid_quality(self, form):
        print("AjaxFormMixin_Quality:form_invalid_quality called. ")
        response = super(AjaxFormMixin_Quality, self).form_invalid(form)
        if self.request.is_ajax():
            print('{}{}'.format("Form Errors: ", form.errors))
            return JsonResponse({'error': [{"field":k, "message": v[0]} for k, v in form.errors.items()]}, status=400)
        else:
            return response

    # Update the object if form is valid
    def form_valid_quality(self, form):
        print("AjaxFormMixin_Quality:form_valid_quality called. ")
        response = super(AjaxFormMixin_Quality, self).form_valid(form)
        print('{}{}'.format("AjaxFormMixin_Quality form_valid_quality ajaxStatus: ", self.request.POST.get('ajaxStatus')))
        print('{}{}'.format("AjaxFormMixin_Quality form_valid_quality request method: ", self.request.method))
        return self.handleAjax(
            self.request,
            form,
            response,
            )

    # This method was writted to override get_context_data to pass additional context data to the view via ajax
    def get_context_data(self, **kwargs):
        print("Cookie: " + settings.CSRF_COOKIE_NAME)
        print("AjaxFormMixin_Quality:get_context_data called.")
        context = super(AjaxFormMixin_Quality, self).get_context_data(**kwargs)
        # paginator = Paginator(self.getQuerySet_Quality(UserToDo), 5) # Show 5 contacts per page
        qualitypage = self.request.GET.get('qualitypage') # Get page from ajax request
        obj = PaintInfo

        print("AjaxFormMixin_Quality:get_context_data called -> request to get general context")
        formInstances = {
            'paintInfo_Form': PaintInfoForm(auto_id='PaintInfoForm_%s'), 
            'batchAdjustment_Form': BatchAdjustmentForm(auto_id='BatchAdjustmentForm_%s'),
            'RDProject_Form' : RDProjectForm(auto_id='RDProjectForm_%s'),
            'productType_Form': ProductTypeForm(auto_id='ProductTypeForm_%s'),
        }
        return self.processPaginatorContext_Quality(Paginator(self.getQuerySet_Quality(obj), 5), formInstances, qualitypage, context)

    def getQuerySet_Quality(self, model, pk=None):
        # If the QuerySet requires a pk
        if pk:
            return get_object_or_404(model, pk=self.kwargs['pk'])
        else:
            return model.objects.order_by('-id')

    def processPaginatorContext_Quality(self, paginatorObject, formInstances, page, context):
        print("Time to paginate quality..")
        try:
            paginatedObjects = paginatorObject.page(page)
            contextData = {**formInstances, 'paginated_Quality':paginatedObjects}
            context.update(contextData)
            print('{}{}'.format("processPaginatorContext_Quality -> page:", page))
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            paginatedObjects = paginatorObject.page(1)
            contextData = {**formInstances, 'paginated_Quality':paginatedObjects}
            context.update(contextData)
            print('{}{}'.format("processPaginatorContext_Quality PageNotAnInteger -> page:", page))
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            paginatedObjects = paginatorObject.page(paginatorObject.num_pages)
            contextData = {**formInstances, 'paginated_Quality':paginatedObjects}
            context.update(contextData)
            print('{}{}'.format("processPaginatorContext_Quality EmptyPage -> page:", page))

        print('{}{}'.format("AjaxFormMixin_Quality:context: ", context))
        return context

    # Method to detect status of form validation for custom Models
    def handleAjax(self, requestObj, form=None, response=None, model=None):
        print("AjaxFormMixin_Quality:handleAjax called.")
        try:

            if requestObj.is_ajax():
                print("AjaxFormMixin_Quality:Process is ajax.")
                if requestObj.method == 'POST':
                    print("AjaxFormMixin_Quality:Process is POST.")
                    if (requestObj.POST.get('ajaxStatus') == "addNewBatchForm"):
                        try:
                            print("AjaxFormMixin_Quality:handleAjax called -> request to add new Batch")
                            obj = PaintInfo( 
                                paintInfoType=form.cleaned_data['paintInfoType'],
                                productType=form.cleaned_data['productType'],
                                rdProject=form.cleaned_data['rdProject'],
                                batchPeriod=form.cleaned_data['batchPeriod'],
                                batchNumber=form.cleaned_data['batchNumber'],
                                batchInsertedBy=User.objects.get(id=requestObj.user.id)
                                )
                            obj.save()

                            print("AjaxFormMixin_Quality: addNewBatchForm complete!")
                            return JsonResponse({'message': "Batch cards inserted!",})
                        except ImproperlyConfigured:
                            JsonResponse({'errorMessage': "Something went wrong trying to create a new Paint Info"})

                    if (requestObj.POST.get('ajaxStatus') == "addRDProject"):
                        try:
                            print("AjaxFormMixin_Quality:handleAjax called -> request to add new RD Project")
                            obj = RDProject( 
                                subject=form.cleaned_data['subject'],
                                customer=form.cleaned_data['customer'],
                                instructions=form.cleaned_data['instructions'],
                                )
                            # obj.save()
                            # obj.customerID.add(CustomerID.objects.get(id=form.cleaned_data['customerID']))
                            obj.save()
                            obj.insertedBy.add(User.objects.get(id=requestObj.user.id))
                            obj.save()
                            print("AjaxFormMixin_Quality: addRDProject complete!")
                            return JsonResponse({'message': "Lab project inserted!",})
                        except ImproperlyConfigured:
                            JsonResponse({'errorMessage': "Something went wrong trying to create a new R&D Project"})

                    if (requestObj.POST.get('ajaxStatus') == "addBatchAdjustment"):
                        try:
                            print("AjaxFormMixin_Quality:handleAjax called -> request to add a batch adjustment")
                            print(form.cleaned_data['adjustmentStage'])
                            obj = FinishingAdjustment(
                                rmCode=form.cleaned_data['rmCode'],
                                adjustmentAmount=form.cleaned_data['adjustmentAmount'],
                                adjustmentUnit=form.cleaned_data['adjustmentUnit'],
                                adjustmentStage=form.cleaned_data['adjustmentStage'],
                                paintInfo=PaintInfo.objects.get(id=requestObj.POST.get('paintInfo'))
                                )
                            # obj.save()
                            # obj.paintInfo.add(PaintInfo.objects.get(id=request.GET.get('paintInfo')))
                            obj.save()
                            obj.insertedBy.add(User.objects.get(id=requestObj.user.id))
                            obj.save()
                            print("AjaxFormMixin_Quality: addBatchAdjustment complete!")
                            return JsonResponse({'message': "Batch adjustment inserted!",})
                        except ImproperlyConfigured:
                            JsonResponse({'errorMessage': "Something went wrong trying to create batch adjustment"})

                    if (requestObj.POST.get('ajaxStatus') == "addProductTypeForm"):
                        try:
                            print("AjaxFormMixin_Quality:handleAjax called -> request to add a product type")
                            obj = ProductType(
                                productCode=form.cleaned_data['productCode'],
                                productDescription=form.cleaned_data['productDescription'],
                                )

                            # obj.save()
                            # obj.paintInfo.add(PaintInfo.objects.get(id=request.GET.get('paintInfo')))
                            obj.save()
                            obj.insertedBy.add(User.objects.get(id=requestObj.user.id))
                            obj.save()
                            print("AjaxFormMixin_Quality: addProductTypeForm complete!")
                            return JsonResponse({'message': "Product type inserted!",})
                        except ImproperlyConfigured:
                            JsonResponse({'errorMessage': "Something went wrong trying to create batch adjustment"})

                    if (requestObj.POST.get('ajaxStatus') == "editPremixInformation"):
                        print("AjaxFormMixin_Quality:handleAjax called -> request to edit premix information")
                        try:
                            # Get object and modify
                            obj = self.getQuerySet_Quality(PaintInfo, pk=self.kwargs['pk'])
                            obj.premixMachine=form.cleaned_data['premixMachine']
                            obj.dateIssued=form.cleaned_data['dateIssued']
                            obj.dateLoaded=form.cleaned_data['dateLoaded']
                            obj.datePremixPassed=form.cleaned_data['datePremixPassed']
                            obj.initialFog=form.cleaned_data['initialFog']
                            obj.initialPremixViscosity=form.cleaned_data['initialPremixViscosity']
                            obj.finalPremixViscosity=form.cleaned_data['finalPremixViscosity']
                            obj.initialViscosityUnit=form.cleaned_data['initialViscosityUnit']
                            obj.finalFog=form.cleaned_data['finalFog']
                            obj.premixInfoModifiedBy = User.objects.get(id=requestObj.user.id)
                            # obj.active=form.cleaned_data['active']
                            obj.save()
                            print("AjaxFormMixin_Quality: editPremixInformation complete!")
                            return JsonResponse({'message': "Premix informaiton modified!",})
                        except ImproperlyConfigured:
                            JsonResponse({'errorMessage': "Something went wrong trying to edit premix information."})

                    if (requestObj.POST.get('ajaxStatus') == "editBatchInformation"):
                        print("AjaxFormMixin_Quality:handleAjax called -> request to edit batch informaiton")
                        try:
                            # Get object and modify
                            obj = self.getQuerySet_Quality(PaintInfo, pk=self.kwargs['pk'])
                            obj.finalSg=form.cleaned_data['finalSg']
                            obj.finalHardDry=form.cleaned_data['finalHardDry']
                            obj.finalHardDryUnit=form.cleaned_data['finalHardDryUnit']
                            obj.finalTouchDry=form.cleaned_data['finalTouchDry']
                            obj.finalTouchDryUnit=form.cleaned_data['finalTouchDryUnit']
                            obj.finalDft=form.cleaned_data['finalDft']
                            obj.finalDftUnit=form.cleaned_data['finalDftUnit']
                            obj.finalOpacity=form.cleaned_data['finalOpacity']
                            obj.finalViscosity=form.cleaned_data['finalViscosity']
                            obj.finalViscosityUnit=form.cleaned_data['finalViscosityUnit']
                            obj.finalGloss=form.cleaned_data['finalGloss']
                            obj.finalColorDe=form.cleaned_data['finalColorDe']
                            obj.finalColorDeSpec=form.cleaned_data['finalColorDeSpec']
                            obj.batchInfoModifiedBy = User.objects.get(id=requestObj.user.id)
                            obj.save()
                            print("AjaxFormMixin_Quality: editBatchInformation complete!")
                            return JsonResponse({'message': "Batch Information modified!",})
                        except ImproperlyConfigured:
                            JsonResponse({'errorMessage': "Something went wrong trying to edit batch information."})
                    
                    if (requestObj.POST.get('ajaxStatus') == "editFinishingAdjustments"):
                        print("AjaxFormMixin_Quality:handleAjax called -> request to edit finishing adjustment")
                        try:
                            # Get object and modify
                            obj = self.getQuerySet_Quality(FinishingAdjustment, pk=self.kwargs['pk'])
                            obj.rmCode=form.cleaned_data['rmCode']
                            obj.adjustmentAmount=form.cleaned_data['adjustmentAmount']
                            obj.adjustmentUnit=form.cleaned_data['adjustmentUnit'] 
                            obj.adjustmentStage=form.cleaned_data['adjustmentStage']
                            obj.paintInfo=PaintInfo.objects.get(id=requestObj.POST.get('paintInfo'))
                            obj.modifiedBy = User.objects.get(id=requestObj.user.id)
                            obj.save()
                            print("AjaxFormMixin_Quality: editFinishingAdjustments complete!")
                            return JsonResponse({'message': "Batch adjustment modified!",})
                        except ImproperlyConfigured:
                            return JsonResponse({'errorMessage': "Something went wrong trying to edit a batch adjustment!",})

                
                    if (requestObj.POST.get('ajaxStatus') == "editRDProject"):
                        print("AjaxFormMixin_Quality:handleAjax called -> request to edit R&D Project")
                        try:
                            # Get object and modify
                            obj = self.getQuerySet_Quality(RDProject, pk=self.kwargs['pk'])
                            obj.subject=form.cleaned_data['subject']
                            obj.customer=form.cleaned_data['customer']
                            obj.instructions=form.cleaned_data['instructions']
                            obj.modifiedBy = User.objects.get(id=requestObj.user.id)
                            obj.save()
                            print("AjaxFormMixin_Quality: editRDProject complete!")
                            return JsonResponse({'message': "Quality project modified!",})
                        except ImproperlyConfigured:
                            return JsonResponse({'errorMessage': "Something went wrong trying to edit a quality adjustment!",})

                    if (requestObj.POST.get('ajaxStatus') == "editBatchProduct"):
                        print("AjaxFormMixin_Quality:handleAjax called -> request to edit R&D Project")
                        try:
                            # Get object and modify
                            obj = self.getQuerySet_Quality(ProductType, pk=self.kwargs['pk'])
                            obj.productCode=form.cleaned_data['productCode']
                            obj.productDescription=form.cleaned_data['productDescription']
                            obj.modifiedBy = User.objects.get(id=requestObj.user.id)
                            obj.save()
                            print("AjaxFormMixin_Quality: editBatchProduct complete!")
                            return JsonResponse({'message': "Batch Product modified!",})
                        except ImproperlyConfigured:
                            return JsonResponse({'errorMessage': "Something went wrong trying to edit a batch product!",})

            else:
                print("AjaxFormMixin_Quality:handleAjax called -> Neither ajax nor form submit...")
                return response

        except ImproperlyConfigured:
            print("ajaxStatus not properly configured.")
            return JsonResponse({'errorMessage': "Something went wrong trying to edit a batch product!",})

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




