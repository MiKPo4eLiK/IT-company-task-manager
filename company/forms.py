from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    """
    Form for creating and updating Task objects.
    This form is used by the TaskCreateView to automatically render form fields
    and handle validation.
    """
    class Meta:
        model = Task
        # You can specify the fields you want to include, or use "__all__" to include all fields.
        fields = "__all__"
