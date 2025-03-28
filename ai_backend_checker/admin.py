# Register your models here.
from django.contrib import admin
<<<<<<< HEAD
from .models import Submission

admin.site.register(Submission)
=======
from .models import Submission ,UserProfile ,Reference

admin.site.register(Submission)
admin.site.register(UserProfile)
admin.site.register(Reference)
>>>>>>> e1dc1b7 (Initial commit)

