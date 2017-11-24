
from django.contrib import admin
from .models import Address, Metro


class MetroAdmin(admin.ModelAdmin):
    list_display = ['line_name', 'station_name', 'line_id', 'station_id', 'lat', 'lng']
    list_filter = ['line_name']
    search_fields = ['line_name', 'station_name']


class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'display_metro_stations', 'city', 'street', 'building', 'description', 'raw', 'lat', 'lng']
#    list_filter = ['filter_metro_stations']
    search_fields = ['street']

    def display_metro_stations(self, obj):
        return "/".join([m.station_name for m in obj.metro_stations.all()])

    display_metro_stations.short_description = 'Станции метро'

    def filter_metro_stations(self, db_field, request, **kwargs):
        if db_field.name == "metro_stations":
            kwargs["queryset"] = Metro.objects.filter(station_id=request.id)
        return super().filter_metro_stations(db_field, request, **kwargs)


admin.site.register(Metro, MetroAdmin)
admin.site.register(Address, AddressAdmin)
