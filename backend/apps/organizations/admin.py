from django.contrib import admin

from organizations.models import Organization

class OrganizationAdmin(admin.ModelAdmin):
    """Организации"""
    list_display = ('__str__', 'kind',)
    list_filter = ('kind',)
    search_fields = ('fullname', 'shortname', 'description',)

admin.site.register(Organization, OrganizationAdmin)