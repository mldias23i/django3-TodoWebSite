from django.db import models
from django.contrib.auth.models import User

# Model class representing a Todo item
class Todo(models.Model):
     # CharField to store the title of the Todo item, with a maximum length of 100 characters
    title = models.CharField(max_length=100)
    # TextField to store additional notes or memo for the Todo item, with an optional blank value
    memo = models.TextField(blank=True)
    # DateTimeField to store the creation date and time of the Todo item, with auto_now_add=True to automatically 
    # set the current date and time when the object is created
    created = models.DateTimeField(auto_now_add=True)
    # DateTimeField to store the date and time when the Todo item is completed, with null=True 
    # and blank=True to allow for empty or null values
    datecompleted = models.DateTimeField(null=True, blank=True)
    # BooleanField to indicate if the Todo item is marked as important, with a default value of False
    important = models.BooleanField(default=False)
    # ForeignKey to establish a one-to-many relationship with the User model, where each Todo item is associated with a specific user
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        # String representation of the Todo object
        return self.title