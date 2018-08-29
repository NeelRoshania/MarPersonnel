from django.contrib.auth.models import User
from home.models import UserToDo, UserNote, NoteDescription
from django import forms


# Create a "Blueprint Form" of how the login form should appear - It interfaces the Django User Class information for Authentication
class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    #Define Meta Data
    class Meta:
        model = User
        #Define fields of the User class that will appear on the form - https://docs.djangoproject.com/en/1.9/ref/contrib/auth/#django.contrib.auth.models.User
        fields = ('username', 'password',)

        widgets = {
        'password': forms.PasswordInput(),
        }

class UserToDoForm(forms.ModelForm): # or forms.ModelForm

    class Meta:
        model = UserToDo
        fields = ('subject', 'toDoProgress')
        
        widgets = {
        'subject': forms.TextInput(attrs={'class':'form-control'}),
        # 'toDoProgress': forms.TextInput(attrs={'class':'datepicker form-control'}),
        'toDoProgress': forms.Select(attrs={'class':'form-control'}),
        }

        labels = {
            "subject": "Subject",
            "toDoProgress" : "Progress",
        }

        error_messages = {
            'subject': {
                'required': ("Subject required!"),
            },
            'toDoProgress': {
                'required': ("Progress of objective required!"),
            },
        }

class UserNoteForm(forms.ModelForm): # or forms.ModelForm

    class Meta:
        model = UserNote
        fields = ('noteProgress', 'taskNote',)
        
        widgets = {
        'taskNote': forms.Textarea(attrs={'class':'form-control', 'cols': 1000, 'rows':2, 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        # 'toDoProgress': forms.TextInput(attrs={'class':'datepicker form-control'}),
        'noteProgress': forms.Select(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        }

        labels = {
            "taskNote": "Note",
            "noteProgress" : "Progress",
        }

        error_messages = {
            'taskNote': {
                'required': ("Description of task required!"),
            },
            'noteProgress': {
                'required': ("Progress of task required!"),
            },
        }

class NoteDescriptionForm(forms.ModelForm): # or forms.ModelForm

    class Meta:
        model = NoteDescription
        fields = ('description', 'noteDescriptionProgress')
        

        widgets = {
        'description': forms.Textarea(attrs={'class':'form-control', 'cols': 1000, 'rows':2, 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        'noteDescriptionProgress': forms.Select(attrs={'class':'form-control', 'style': "width: 100% !important; margin-bottom: 0.7em"}),
        }

        labels = {
            "description": "Description",
            "noteDescriptionProgress": "Progress"
        }

        error_messages = {
            'description': {
                'required': ("Description of note required!"),
            },
            'noteDescriptionProgress': {
                'required': ("Progress of note required!"),
            },
        }
