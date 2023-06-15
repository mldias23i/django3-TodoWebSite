from django.forms import ModelForm
from .models import Todo

# Form class for creating and updating Todo objects
class TodoForm(ModelForm):
    # Meta class for specifying the form's metadata
    class Meta:
        # Specify the model that the form is associated with, which is the Todo model
        model = Todo
        # Specify the fields to include in the form, which are 'title', 'memo', and 'important'
        fields = ['title', 'memo', 'important']