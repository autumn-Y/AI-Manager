from django.contrib import admin
from .models import Recent
from .models import Goal
from .models import User
# Register your models here.

admin.site.register(Recent)
admin.site.register(Goal)
admin.site.register(User)
