from django.contrib import admin
from .models import House, Intercom, Apartment


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ["number", "house"]
    

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ["street", "number"]


@admin.register(Intercom)
class IntercomAdmin(admin.ModelAdmin):
    list_display = ["name", "date_setup", "house"]