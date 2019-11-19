from django.contrib import admin
from .models import Group,Comment,Profile

admin.site.register(Group)
admin.site.register(Profile)
admin.site.register(Comment)
