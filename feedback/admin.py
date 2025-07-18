from django.contrib import admin
from .models import Course, Feedback

admin.site.register(Course)
admin.site.register(Feedback)

Course.objects.bulk_create([
    Course(name='Python'),
    Course(name='Data Structures'),
    Course(name='Machine Learning'),
    Course(name='Web Development'),
    Course(name='DBMS'),
    Course(name='Networking'),
    Course(name='AI Ethics'),
    Course(name='Cloud Computing')
])
