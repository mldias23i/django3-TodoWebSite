from django.contrib import admin
from .models import Todo

class TodoAdmin(admin.ModelAdmin):
    # Set the 'created' field as readonly
    readonly_fields = ('created',)

# Register the Todo model with the TodoAdmin configuration
admin.site.register(Todo, TodoAdmin)