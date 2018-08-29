from django.db import models
from production.models import ProdMeeting, ProdNote, RMShortage
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy 
# Create your models here.

# User Note Object Mode
class UserToDo(models.Model):
	PROGRESS = (
    ('In Progress', 'In Progress'),
    ('Completed', 'Completed'),
	)
	subject = models.CharField(max_length=150, blank=False)
	insertedAt = models.DateTimeField(auto_now_add=True)
	toDoProgress = models.CharField(max_length=20, choices=PROGRESS, blank=False)
	generatedBy = models.ManyToManyField(User)
	modifiedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_userToDo', null=True)
	dateCompleted = models.DateTimeField(auto_now=True)

	def getUserNotes(self):
		return UserNote.objects.filter(UserToDo=self.id).order_by('-id')

	def __str__(self):
		return self.subject

	def get_absolute_url(self):
		return reverse('home:index')

	class Meta:
		ordering = ['subject']

#Production Note Class
class UserNote(models.Model):

	PROGRESS = (
    ('In Progress', 'In Progress'),
    ('Completed', 'Completed'),
	)

	FIELDS = (
    ('Contact Person', 'Contact Person'),
    ('Contact Email', 'Contact Email'),
    ('Contact Number', 'Contact Number'),
    ('Company Name', 'Company Name'),
    ('Other', 'Other'),
    ('Note', 'Note'),
	)
	taskStatus = models.CharField(max_length=20, choices=FIELDS, blank=False)
	taskNote = models.TextField(max_length=200, blank=False)
	UserToDo = models.ManyToManyField(UserToDo, blank=False)
	noteProgress = models.CharField(max_length=20, choices=PROGRESS, blank=False)
	generatedBy = models.ManyToManyField(User)
	modifiedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_Note', null=True)
	insertedAt = models.DateTimeField(auto_now_add=True)
	dateCompleted = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.taskNote

	def getNoteDescriptions(self):
		return NoteDescription.objects.filter(userNote=self.id).order_by('-id')

	def get_absolute_url(self):
		# return reverse('paint-add', kwargs={'pk': self.pk})
		return reverse('home:index')

#Production Note Class
class NoteDescription(models.Model):

	PROGRESS = (
    ('In Progress', 'In Progress'),
    ('Completed', 'Completed'),
	)
	
	description = models.CharField(max_length=100, blank=False)
	userNote = models.ForeignKey(UserNote, on_delete=models.CASCADE)
	noteDescriptionProgress = models.CharField(max_length=20, choices=PROGRESS, blank=False)
	generatedBy = models.ManyToManyField(User)
	modifiedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_NoteDescription', null=True)
	insertedAt = models.DateTimeField(auto_now_add=True)
	dateCompleted = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.description

	def get_absolute_url(self):
		# return reverse('paint-add', kwargs={'pk': self.pk})
		return reverse('home:index')