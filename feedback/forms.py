from django import forms
from .models import Feedback, Course
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class TailwindFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': field.label
            })

class RegisterForm(TailwindFormMixin, UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

RATING_CHOICES = [
    (1, '⭐☆☆☆☆'),
    (2, '⭐⭐☆☆☆'),
    (3, '⭐⭐⭐☆☆'),
    (4, '⭐⭐⭐⭐☆'),
    (5, '⭐⭐⭐⭐⭐'),
]

class FeedbackForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['course', 'rating', 'comments']
        widgets = {
            'course': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'rating': forms.Select(choices=RATING_CHOICES, attrs={'class': 'w-full p-2 border rounded'}),
            'comments': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        courses = Course.objects.all().order_by('name')
        unique_courses = {}
        for course in courses:
            if course.name not in unique_courses:
                unique_courses[course.name] = course

        self.fields['course'].queryset = Course.objects.filter(id__in=[c.id for c in unique_courses.values()])
