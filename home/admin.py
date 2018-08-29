from django.contrib import admin
from .models import UserToDo, UserNote, NoteDescription

# Register your models here.
admin.site.register(UserToDo)
admin.site.register(UserNote)
admin.site.register(NoteDescription)
