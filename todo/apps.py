from django.apps import AppConfig

# Configuration class for the 'todo' app
class TodoConfig(AppConfig):
    # Set the default auto-generated primary key field to 'BigAutoField'
    default_auto_field = 'django.db.models.BigAutoField'
    # Specify the name of the app
    name = 'todo'
