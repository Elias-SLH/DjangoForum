from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Question, Answer


UserAdmin.list_display = ['username', 'is_staff', 'is_active']


admin.site.register(Question)
admin.site.register(Answer)
