from django.contrib.auth.models import User
from .models import RDProject, ProductType, PaintInfo, FinishingAdjustment
from django import forms


class PaintInfoForm(forms.ModelForm): # or forms.ModelForm

    class Meta:
        model = PaintInfo

        fields = (
            'paintInfoType',
            'productType',
            'premixMachine',
            'rdProject',
            'batchPeriod',
            'batchNumber',
            'initialFog',
            'initialFogUnit',
            'initialPremixViscosity',
            'initialViscosityUnit',
            'finalSg',
            'finalHardDry',
            'finalHardDryUnit',
            'finalTouchDry',
            'finalTouchDryUnit',
            'finalDft',
            'finalFOGUnit',
            'finalDftUnit',
            'finalOpacity',
            'finalFog',
            'finalViscosity',
            'finalViscosityUnit',
            'finalGloss',
            'finalColorDe',
            'finalColorDeSpec',
            'dateIssued',
            'dateLoaded',
            'datePremixPassed',
            'active',
        )

        labels = {
            'paintInfoType': "Batch type",
            'productType': "Name of product",
            'premixMachine': "Grind Machine",
            'rdProject': "R&D project assigned to",
            'batchPeriod': "Batch period",
            'batchNumber': "Batch number",
            'initialFog': "Premix FOG",
            'initialFogUnit': "Premix FOG specification",
            'initialPremixViscosity': "Initial premix viscosity",
            'finalPremixViscosity': "Final premix viscosity",
            'initialViscosityUnit': "Premix viscosity unit",
            'finalSg': "Specific gravity at pass",
            'finalHardDry': "Hard dry at pass",
            'finalHardDryUnit': "Hard dry unit",
            'finalTouchDry': "Touch dry at pass",
            'finalTouchDryUnit': "Touch dry unit",
            'finalDft': "Dry film thickness at pass",
            'finalDftUnit': "Dry film thickness unit",
            'finalOpacity': "Opacity at pass",
            'finalFog': "Final FOG at pass",
            'finalFOGUnit': "Final FOG specification",
            'finalViscosity': "Final viscosity at pass",
            'finalViscosityUnit': "Final viscosity at pass",
            'finalGloss': "Final gloss at pass",
            'finalColorDe': "Final color DE at pass",
            'finalColorDeSpec': "Color passed on:",
            'dateIssued': "Date of batch card issue:",
            'dateLoaded': "Date of premix load",
            'datePremixPassed': "Date of premix pass",
            'active': "Status of batch",
        }

        widgets = {
            'paintInfoType': forms.Select(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'premixMachine': forms.Select(attrs={'class':'form-control'}),
            'productType': forms.Select(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'rdProject': forms.Select(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'batchPeriod': forms.NumberInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'batchNumber': forms.NumberInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'initialFog': forms.NumberInput(attrs={'class':'form-control'}),
            'initialFogUnit': forms.Select(attrs={'class':'form-control',}),
            'initialPremixViscosity': forms.NumberInput(attrs={'class':'form-control'}),
            'finalPremixViscosity': forms.NumberInput(attrs={'class':'form-control'}),
            'initialViscosityUnit': forms.Select(attrs={'class':'form-control'}),
            'finalSg': forms.NumberInput(attrs={'class':'form-control'}),
            'finalHardDry': forms.NumberInput(attrs={'class':'form-control'}),
            'finalHardDryUnit': forms.Select(attrs={'class':'form-control'}),
            'finalTouchDry': forms.NumberInput(attrs={'class':'form-control'}),
            'finalTouchDryUnit': forms.Select(attrs={'class':'form-control'}),
            'finalDft': forms.NumberInput(attrs={'class':'form-control'}),
            'finalDftUnit': forms.Select(attrs={'class':'form-control'}),
            'finalOpacity': forms.NumberInput(attrs={'class':'form-control'}),
            'finalFog': forms.NumberInput(attrs={'class':'form-control'}),
            'finalFOGUnit': forms.Select(attrs={'class':'form-control'}),
            'finalViscosity': forms.NumberInput(attrs={'class':'form-control'}),
            'finalViscosityUnit': forms.Select(attrs={'class':'form-control'}),
            'finalGloss': forms.NumberInput(attrs={'class':'form-control'}),
            'finalColorDe': forms.NumberInput(attrs={'class':'form-control'}),
            'finalColorDeSpec': forms.Select(attrs={'class':'form-control'}),
            'dateIssued': forms.TextInput(attrs={'class':'datepicker date form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'dateLoaded': forms.TextInput(attrs={'class':'datepicker date form-control'}),
            'datePremixPassed': forms.TextInput(attrs={'class':'datepicker date form-control'}),
            'active': forms.Select(attrs={'class':'form-control'}),
        }

        error_messages = {
            'paintInfoType': {
                'required': ("Batch type required!"),
            },
            'productType': {
                'required': ("Product type required!"),
            },
            'batchPeriod': {
                'required': ("Batch period required!"),
            },
            'batchNumber': {
                'required': ("Batch number required!"),
            },
            'dateIssued': {
                'required': ("Date of batch issue required!"),
            },

        }

    def clean_batchPeriod(self):
        batchPeriod = self.cleaned_data.get('batchPeriod')
        if batchPeriod >= 999:
            raise forms.ValidationError('Batch period format incorrect!')
        return batchPeriod

    def clean_batchNumber(self):
        batchNumber = self.cleaned_data.get('batchNumber')
        if batchNumber >= 99999:
            raise forms.ValidationError('Batch number format incorrect!')
        return batchNumber

class PremixInfoForm(forms.ModelForm): # or forms.ModelForm

    class Meta:
        model = PaintInfo

        fields = (
            'initialFog',
            'initialFogUnit',
            'initialPremixViscosity',
            'finalPremixViscosity',
            'initialViscosityUnit',
            'finalFog',
            'finalFOGUnit',
            'dateLoaded',
            'datePremixPassed',
            'premixMachine',
            # 'active',
        )

        labels = {
            'initialFog': "Premix FOG",
            'initialFogUnit': "Initial premix viscosity specification",
            'initialPremixViscosity': "Initial premix viscosity",
            'finalPremixViscosity': "Final premix viscosity",
            'initialViscosityUnit': "Premix viscosity unit",
            'finalFog': "Final FOG at pass",
            'finalFOGUnit': "Final FOG specification",
            'dateLoaded': "Date of premix load",
            'datePremixPassed': "Date of premix pass",
            'premixMachine': "Premix Machine",
            # 'active': "Status of batch",
        }

        widgets = {
            'initialFog': forms.NumberInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'initialFogUnit': forms.Select(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'initialPremixViscosity': forms.NumberInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em", 'step': '0.01'}),
            'finalPremixViscosity': forms.NumberInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em", 'step': '0.01'}),
            'initialViscosityUnit': forms.Select(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'finalFog': forms.NumberInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em", 'step': '1'}),
            'finalFOGUnit': forms.Select(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'dateLoaded': forms.TextInput(attrs={'class':'datepicker date form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'datePremixPassed': forms.TextInput(attrs={'class':'datepicker date form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'premixMachine': forms.Select(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            # 'active': forms.Select(attrs={'class':'form-control'}),
        }

    # def clean_initialPremixViscosity(self):
    #     i_Visc = self.cleaned_data.get('initialPremixViscosity')
    #     if i_Visc is None:
    #         raise forms.ValidationError('Initial viscosity required!')
    #     return i_Visc

    # def clean_finalPremixViscosity(self):
    #     i_Visc = self.cleaned_data.get('finalPremixViscosity')
    #     if i_Visc is None:
    #         raise forms.ValidationError('Final viscosity required!')
    #     return i_Visc

    # def clean_finalViscosity(self):
    #     i_Visc = self.cleaned_data.get('finalPremixViscosity')
    #     if i_Visc is None:
    #         raise forms.ValidationError('Final premix viscosity required!')
    #     return i_Visc

    def clean_initialViscosityUnit(self):
        iViscUnit = self.cleaned_data.get('initialViscosityUnit')
        if iViscUnit is None:
            raise forms.ValidationError('Viscosity specification required!')
        return iViscUnit
    
    def clean_initialFogUnit(self):
        iFOG_Unit = self.cleaned_data.get('initialFogUnit')
        if iFOG_Unit is None:
            raise forms.ValidationError('Initial FOG specification required!')
        return iFOG_Unit


    def clean_finalFOGUnit(self):
        fFog_Unit = self.cleaned_data.get('finalFOGUnit')
        if fFog_Unit is None:
            raise forms.ValidationError('Final FOG specification required!')
        return fFog_Unit

    def clean_dateLoaded(self):
        d_loaded = self.cleaned_data.get('dateLoaded')
        if d_loaded is None:
            raise forms.ValidationError('Date loaded required!')
        return d_loaded

    def clean_datePremixPassed(self):
        d_premixPassed = self.cleaned_data.get('datePremixPassed')
        if d_premixPassed is None:
            raise forms.ValidationError('Premix pass date required!')
        return d_premixPassed

class BatchInfoForm(forms.ModelForm): # or forms.ModelForm

    class Meta:
        model = PaintInfo

        fields = (
            'finalSg',
            'finalHardDry',
            'finalHardDryUnit',
            'finalTouchDry',
            'finalTouchDryUnit',
            'finalDft',
            'finalDftUnit',
            'finalOpacity',
            'finalViscosity',
            'finalViscosityUnit',
            'finalGloss',
            'finalColorDe',
            'finalColorDeSpec',
        )

        labels = {
            'finalSg': "Specific gravity at pass",
            'finalHardDry': "Hard dry at pass",
            'finalHardDryUnit': "Hard dry unit",
            'finalTouchDry': "Touch dry at pass",
            'finalTouchDryUnit': "Touch dry unit",
            'finalDft': "Dry film thickness at pass",
            'finalDftUnit': "Dry film thickness unit",
            'finalOpacity': "Opacity at pass",
            'finalViscosity': "Final viscosity at pass",
            'finalViscosityUnit': "Final viscosity at pass",
            'finalGloss': "Final gloss at pass",
            'finalColorDe': "Final color DE at pass",
            'finalColorDeSpec': "Color passed on:",
        }

        widgets = {
            'finalSg': forms.NumberInput(attrs={'class':'form-control', 'step': '0.001', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'finalHardDry': forms.NumberInput(attrs={'class':'form-control', 'step': '0.01', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'finalHardDryUnit': forms.Select(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'finalTouchDry': forms.NumberInput(attrs={'class':'form-control', 'step': '0.01', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'finalTouchDryUnit': forms.Select(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'finalDft': forms.NumberInput(attrs={'class':'form-control', 'step': '0.01', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'finalDftUnit': forms.Select(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'finalOpacity': forms.NumberInput(attrs={'class':'form-control', 'step': '0.01', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'finalViscosity': forms.NumberInput(attrs={'class':'form-control', 'step': '0.01', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'finalViscosityUnit': forms.Select(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'finalGloss': forms.NumberInput(attrs={'class':'form-control', 'step': '0.01', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'finalColorDe': forms.NumberInput(attrs={'class':'form-control', 'step': '0.001', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'finalColorDeSpec': forms.Select(attrs={'class':'form-control', 'step': '0.001', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        }

    def clean_finalSG(self):
        f_SG = self.cleaned_data.get('finalSG')
        if f_SG is None:
            raise forms.ValidationError('Final specific gravity required!')
        return f_SG

    # def clean_finalHardDry(self):
    #     f_HardDry = self.cleaned_data.get('finalHardDry')
    #     if f_HardDry is None:
    #         raise forms.ValidationError('Final hard dry time required!')
    #     return f_HardDry

    def clean_finalHardDryUnit(self):
        f_HardDryUnit = self.cleaned_data.get('finalHardDryUnit')
        if f_HardDryUnit is None:
            raise forms.ValidationError('Final hard dry unit required!')
        return f_HardDryUnit

    # def clean_finalTouchDry(self):
    #     f_TouchDry = self.cleaned_data.get('finalTouchDry')
    #     if f_TouchDry is None:
    #         raise forms.ValidationError('Final touch dry time required!')
    #     return f_TouchDry

    def clean_finalTouchDryUnit(self):
        f_TouchDryUnit = self.cleaned_data.get('finalTouchDryUnit')
        if f_TouchDryUnit is None:
            raise forms.ValidationError('Final Touch dry unit required!')
        return f_TouchDryUnit

    # def clean_finalDft(self):
    #     f_DFT = self.cleaned_data.get('finalDft')
    #     if f_DFT is None:
    #         raise forms.ValidationError('Final DFT required!')
    #     return f_DFT

    # def clean_finalDftUnit(self):
    #     f_DftUnit = self.cleaned_data.get('finalDftUnit')
    #     if f_DftUnit is None:
    #         raise forms.ValidationError('Final DFT unit required!')
    #     return f_DftUnit

    # def clean_finalOpacity(self):
    #     f_Opacity = self.cleaned_data.get('finalOpacity')
    #     if f_Opacity is None:
    #         raise forms.ValidationError('Final opacity required!')
    #     return f_Opacity

    # def clean_finalViscosity(self):
    #     f_Visc = self.cleaned_data.get('finalViscosity')
    #     if f_Visc is None:
    #         raise forms.ValidationError('Final viscosity required!')
    #     return f_Visc

    def clean_finalViscosityUnit(self):
        f_ViscUnit = self.cleaned_data.get('finalViscosityUnit')
        if f_ViscUnit is None:
            raise forms.ValidationError('Final viscosity unit required!')
        return f_ViscUnit

    # def clean_finalGloss(self):
    #     f_gloss = self.cleaned_data.get('finalGloss')
    #     if f_gloss is None:
    #         raise forms.ValidationError('Final gloss required!')
    #     return f_gloss

    # def clean_finalColorDe(self):
    #     f_ColorDe = self.cleaned_data.get('finalColorDe')
    #     if f_ColorDe is None:
    #         raise forms.ValidationError('Final color DE required!')
    #     return f_ColorDe

    def clean_finalColorDeSpec(self):
        f_ColorDESpec = self.cleaned_data.get('finalColorDeSpec')
        if f_ColorDESpec is None:
            raise forms.ValidationError('Final color DE specification required!')
        return f_ColorDESpec

class RDProjectForm(forms.ModelForm): # or forms.ModelForm

    class Meta:
        model = RDProject

        fields = (
            'customer',
            'subject',
            'instructions',
            )

        labels = {
            'customer': "Customer",
            'subject': "Subject",
            'instructions': "Instructions/notes",
        }

        widgets = {
            'customer': forms.Select(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'subject': forms.TextInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'instructions': forms.Textarea(attrs={'class':'form-control', 'cols': 1000, 'rows':1, 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        }

        error_messages = {
            'customer': {
                'required': ("Customer required!"),
            },
            'subject': {
                'required': ("Subject required!"),
            },
            'instructions': {
                'required': ("Instructions required!"),
            },
        }

class ProductTypeForm(forms.ModelForm): # or forms.ModelForm

    class Meta:
        model = ProductType

        fields = (
            'productCode',
            'productDescription',
            )

        labels = {
        'productCode': "Product code",
        'productDescription': "Product description",
        }

        widgets = {
            'productCode': forms.TextInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'productDescription': forms.TextInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        }

        error_messages = {
            'productCode': {
                'required': ("Product code required!"),
            },
            'productDescription': {
                'required': ("Product description required!"),
            },
        }

class BatchAdjustmentForm(forms.ModelForm): # or forms.ModelForm

    class Meta:
        model = FinishingAdjustment

        fields = (
            'rmCode',
            'adjustmentAmount',
            'adjustmentUnit',
            'adjustmentStage',
            )

        labels = {
            'rmCode': "Raw material code",
            'adjustmentAmount': "Raw material description",
            'adjustmentUnit': "Raw material description",
            'adjustmentStage': "Stage of adjustment",
        }

        widgets = {
            'rmCode': forms.Select(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'adjustmentAmount': forms.NumberInput(attrs={'class':'form-control', 'step': '0.01', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'adjustmentUnit': forms.Select(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
            'adjustmentStage': forms.Select(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}), 
        }

        error_messages = {
            'rmCode': {
                'required': ("Raw material code required!"),
            },
            'adjustmentAmount': {
                'required': ("Raw material adjustment amount required!"),
            },
            'adjustmentUnit': {
                'required': ("Raw material adjustment unit required!"),
            },
            'adjustmentStage': {
                'required': ("Adjustment stage required!"),
            },
        }









