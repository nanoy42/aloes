from django.contrib import admin

from .models import Leasing, Map, Renovation, Rent, Room, School, Tenant

admin.site.register(School)
admin.site.register(Renovation)
admin.site.register(Rent)
admin.site.register(Tenant)
admin.site.register(Room)
admin.site.register(Leasing)
admin.site.register(Map)
