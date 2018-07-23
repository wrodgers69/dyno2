from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Card_Info, Well_Profile, Dysfunction_Profile

admin.site.register(Card_Info)
admin.site.register(Well_Profile)
admin.site.register(Dysfunction_Profile)
