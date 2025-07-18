from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, FeedbackForm
from .models import Feedback

def home(request):
    return render(request, 'feedback/home.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'feedback/register.html', {'form': form})

@login_required
def dashboard(request):
    feedbacks = Feedback.objects.filter(user=request.user)
    return render(request, 'feedback/dashboard.html', {'feedbacks': feedbacks})

@login_required
def give_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('dashboard')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/give_feedback.html', {'form': form})
