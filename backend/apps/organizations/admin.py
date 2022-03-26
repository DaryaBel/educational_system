from django.contrib import admin

from organizations.models import City, Organization, OrganizationCity

class OrganizationCityInline(admin.StackedInline):
    model = OrganizationCity
    extra = 0

class OrganizationAdmin(admin.ModelAdmin):
    """Организации"""
    list_display = ('__str__', 'type',)
    list_filter = ('type',)
    search_fields = ('fullname', 'shortname', 'description',)
    inlines = [OrganizationCityInline]

class CityAdmin(admin.ModelAdmin):
    """Города"""
    list_display = ('__str__',)
    search_fields = ('name',)


admin.site.register(City, CityAdmin)
admin.site.register(Organization, OrganizationAdmin)