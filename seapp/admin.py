from django.contrib import admin
from seapp.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Photo)
admin.site.register(Submission)
admin.site.register(Skipped)
