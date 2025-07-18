from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, FeedbackForm
from .models import Feedback, Course

def home(request):
    """Render the homepage."""
    return render(request, 'feedback/home.html')


def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'feedback/register.html', {'form': form})


@login_required
def dashboard(request):
    """Display user's submitted feedback."""
    feedbacks = Feedback.objects.filter(user=request.user).order_by('-submitted_at')
    return render(request, 'feedback/dashboard.html', {'feedbacks': feedbacks})


@login_required
def give_feedback(request):
    """Allow user to submit feedback."""
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user  # Assign the logged-in user
            feedback.save()
            messages.success(request, "Feedback submitted successfully!")
            return redirect('dashboard')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/give_feedback.html', {'form': form})


@login_required
def delete_feedback(request, pk):
    """Delete a user's feedback."""
    feedback = get_object_or_404(Feedback, pk=pk, user=request.user)
    if request.method == 'POST':
        feedback.delete()
        messages.success(request, 'Feedback deleted successfully!')
        return redirect('dashboard')
    return render(request, 'feedback/confirm_delete.html', {'feedback': feedback})
