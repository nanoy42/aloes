"""Admin for aloes app."""
from django.contrib import admin

from .models import GeneralPreferences

admin.site.register(GeneralPreferences)
