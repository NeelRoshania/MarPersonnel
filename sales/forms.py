from django.contrib.auth.models import User
from .models import CustomerID, DeliveryPlan
from django import forms


class DeliveryPlanForm(forms.ModelForm): # or forms.ModelForm

    class Meta:
        model = DeliveryPlan
        fields = ('customerID', 'dateOfDelivery', 'orderDate', 'invoiceNumber', 'active', 'delayField', 'delayReason',)

        labels = {
            "customerID": "Customer",
            "orderDate" : "Order placed on",
            'dateOfDelivery': "Date to be delivered",
            'invoiceNumber' : "Invoice number",
            'active': 'Status',
            'delayField': "Catagory of delay (if applicable)",
            'delayReason': "Reason for delay (if applicable)"
        }

        widgets = {
        'customerID': forms.Select(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'subject': forms.TextInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'orderDate': forms.TextInput(attrs={'class':'datepicker date form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'dateOfDelivery': forms.TextInput(attrs={'class':'datepicker date form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'invoiceNumber': forms.TextInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'active': forms.Select(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'delayField': forms.Select(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'delayReason': forms.TextInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        }

        error_messages = {
            'customerID': {
                'required': ("Customer required!"),
            },
            'dateOfDelivery': {
                'required': ("Delivery date required!"),
            },
            'orderDate': {
                'required': ("Order date required!"),
            },
            'invoiceNumber': {
                'required': ("Invoice number required!"),
            },
            'active': {
                'required': ("Status required!"),
            },
        }

class CustomerIDForm(forms.ModelForm): # or forms.ModelForm

    class Meta:
        model = CustomerID
        fields = (
            'customerCode', 
            'customerName', 
            'procurementName', 
            'procurementWorkNum', 
            'procurementWorkEmail', 
            'technicalWorkNum', 
            'technicalName', 
            'technicalWorkEmail', 
            'customerType',
            'customerStatus',
            )

        labels = {
            "customerCode": "Marindec account number",
            'customerName': "Company name",
            'procurementName' : "Buyer name",
            'procurementWorkNum': 'Buyer work number',
            'procurementWorkEmail': "Buyer work email",
            'technicalName' : "Technical name",
            'technicalWorkNum': "Technical work number",
            'technicalWorkEmail': "Technical work email",
            'technicalWorkNum': "Technical work contact",
            'customerType': "Type of customer",
            'customerStatus': "Activity of customer",
        }

        widgets = {
        'customerCode': forms.TextInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'customerName': forms.TextInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'procurementName': forms.TextInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'procurementWorkNum': forms.TextInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'procurementWorkEmail': forms.TextInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'technicalName': forms.TextInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'technicalWorkEmail': forms.TextInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'technicalWorkNum': forms.TextInput(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'customerType': forms.Select(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'customerStatus': forms.Select(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        }

        error_messages = {
            'customerCode': {
                'required': ("Customer code required!"),
            },
            'customerName': {
                'required': ("Customer name required!"),
            },
            'procurementName': {
                'required': ("Buyer name required!"),
            },
            'procurementWorkNum': {
                'required': ("Buyer contact number required!"),
            },
            'procurementWorkEmail': {
                'required': ("Buyer email required!"),
                'invalid': ("Buyer email address invalid!"),
            },
            'customerType': {
                'required': ("Customer type required!"),
            },
            'customerStatus': {
                'required': ("Customer activity required!"),
            },
        }










