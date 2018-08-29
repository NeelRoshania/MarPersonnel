from django.contrib.auth.models import User
from .models import ProdMeeting, ProdNote, ProductionPlan, RMShortage, RMReference, MaintenanceIssue
from django import forms


class ProductionMeetingForm(forms.ModelForm): # or forms.ModelForm

    class Meta:
        model = ProdMeeting
        fields = ('subject',)

        labels = {
            "subject": "Subject of meeting",
        }

        widgets = {
        'subject': forms.TextInput(attrs={'class':'form-control'}),
        # 'toDoProgress': forms.TextInput(attrs={'class':'datepicker form-control'}),
        # 'toDoProgress': forms.Select(attrs={'class':'form-control'}),
        }

        error_messages = {
            'subject': {
                'required': ("Subject of meeting required!"),
            },
        }

class ProductionNoteForm(forms.ModelForm): # or forms.ModelForm

    class Meta:
        model = ProdNote
        fields = ('prodNote',)
        
        labels = {
            "prodNote": "Production note",
        }

        widgets = {
        'prodNote': forms.Textarea(attrs={'class':'form-control', 'cols': 1000, 'rows':5, 'style': "width: 100% !important;"}),
        }

        error_messages = {
            'prodNote': {
                'required': ("Production note required!"),
            },
        }

class RMReferenceForm(forms.ModelForm): # or forms.ModelForm

    class Meta:
        model = RMReference

        fields = ('rmCode', 'rmDescription')

        labels = {
            "rmCode": "Raw material code",
            "rmDescription": "Raw material description",
        }

        widgets = {
        'rmCode': forms.TextInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'rmDescription': forms.TextInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        }

        error_messages = {
            'rmCode': {
                'required': ("Code of raw material required!"),
            },
            'rmDescription': {
                'required': ("Description of shortage required!"),
            },
        }
        
class RMShortageForm(forms.ModelForm): # or forms.ModelForm

    class Meta:
        model = RMShortage
        fields = ('rmShortage', 'rmLevel', 'rmStatus')
        
        labels = {
            "rmShortage": "Name of raw material",
            "rmLevel": "Level of shortage",
            "rmStatus": "Status of shortage",
        }

        widgets = {
        'rmShortage': forms.SelectMultiple( attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'rmStatus': forms.Select(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'rmLevel': forms.TextInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        # 'noteProgress': forms.Select(attrs={'class':'form-control'}),
        }

        error_messages = {
            'rmShortage': {
                'required': ("Name of raw material required!"),
            },
            'rmStatus': {
                'required': ("Status of shortage required!"),
            },
        }

class MaintenanceIssueForm(forms.ModelForm): # or forms.ModelForm

    class Meta:
        model = MaintenanceIssue
        fields = ('maintenanceType', 'subject', 'active', 'note')
        labels = {
            "maintenanceType": "Type of maintenance issue",
            "subject": "Description of issue",
            "active": "Status",
            "note": "Action required",
        }

        widgets = {
        'maintenanceType': forms.Select( attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'subject': forms.TextInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'active': forms.Select( attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'note': forms.TextInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        # 'noteProgress': forms.Select(attrs={'class':'form-control'}),
        }

        error_messages = {
            'maintenanceType': {
                'required': ("Type of issue required!"),
            },
            'subject': {
                'required': ("Subject required!"),
            },
            'note': {
                'required': ("Action required!"),
            },
            'active': {
                'required': ("Status required!"),
            },
        }

class ProductionPlanForm(forms.ModelForm): # or forms.ModelForm

    class Meta:
        model = ProductionPlan
        fields = ('machine', 'batchNumber', 'productDescription', 'status')
        labels = {
            "machine": "Machine",
            "batchNumber": "Batch Number (e.g 233/12345)",
            "productDescription": "Description of product",
            "status": "Status of plan",
        }

        widgets = {
        'machine': forms.Select( attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'batchNumber': forms.TextInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'productDescription': forms.TextInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'status': forms.Select( attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        # 'noteProgress': forms.Select(attrs={'class':'form-control'}),
        }

        error_messages = {
            'machine': {
                'required': ("Machine required!"),
            },
            'batchNumber': {
                'required': ("Batch number required!"),
            },
            'productDescription': {
                'required': ("Product description required!"),
            },
            'status': {
                'required': ("Status required!"),
            },
        }