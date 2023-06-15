from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    # Renders the home.html template
    return render(request, 'todo/home.html')

def signupUser(request):
    # Renders the signupUser.html template with a UserCreationForm instance
    if request.method == 'GET':
        return render(request, 'todo/signupUser.html', {'form':UserCreationForm()})
    else:
        # Create a new user
        if request.POST['password1'] == request.POST['password2']:
            # Attempt to create a new user with the provided username and password
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentTodos')
            # If the username already exists, render the signupUser.html template with an error message
            except IntegrityError:
                return render(request, 'todo/signupUser.html', {'form':UserCreationForm(), 'error': 'That username has already been taken. Please choose a new username'})
        else:
            # If the passwords do not match, render the signupUser.html template with an error message
            return render(request, 'todo/signupUser.html', {'form':UserCreationForm(), 'error': 'Passwords did not match'})


def logInUser(request):
    # Renders the logInUser.html template with an AuthenticationForm instance
    if request.method == 'GET':
        return render(request, 'todo/logInUser.html', {'form':AuthenticationForm()})
    # Authenticate the user with the provided username and password
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        # If authentication fails, render the logInUser.html template with an error message
        if user is None:
            return render(request, 'todo/logInUser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match!'})
        else:
            # If authentication succeeds, log in the user and redirect to the currentTodos view
            login(request, user)
            return redirect('currentTodos')


@login_required
def logoutUser(request):
    # Log out the user and redirect to the home view
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    
@login_required
def createTodo(request):
    # Renders the createTodo.html template with a TodoForm instance
    if request.method == 'GET':
        return render(request, 'todo/createTodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newTodo = form.save(commit=False)
            newTodo.user = request.user
            newTodo.save()
            return redirect('currentTodos')
        # If the form data is invalid, render the createTodo.html template with an error message
        except ValueError:
            return render(request, 'todo/createTodo.html', {'form':TodoForm(), 'error':'Bad data passed in. Try again! '})
        
@login_required
# Get all the current Todo items for the authenticated user
def currentTodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currentTodos.html', {'todos':todos})

@login_required
# Get all the completed Todo items for the authenticated user
def completedTodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedTodos.html', {'todos':todos})

@login_required
def viewtodo(request, todo_pk):
    # Retrieve the Todo object with the specified primary key (todo_pk) and owned by the authenticated user
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    # If the request method is GET, create a TodoForm instance with the retrieved Todo object and render the 
    # viewtodo.html template
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
    else:
        # If the request method is not GET, 
        # create a TodoForm instance with the form data and the retrieved Todo object
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currentTodos')
        # If there is a ValueError, render the viewtodo.html template with the error message
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form, 'error':'Bad info! '})        
        
@login_required
def completeTodo(request, todo_pk):
    # Retrieve the Todo object with the specified primary key (todo_pk) and owned by the authenticated user
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    # If the request method is POST, mark the Todo as completed by setting the datecompleted field to 
    # the current time and save the Todo object
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currentTodos')

@login_required
def deleteTodo(request, todo_pk):
    # Retrieve the Todo object with the specified primary key (todo_pk) and owned by the authenticated user
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    # If the request method is POST, delete the Todo object and redirect to the currentTodos view
    if request.method == 'POST':
        todo.delete()
        return redirect('currentTodos')
