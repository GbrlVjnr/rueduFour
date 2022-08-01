from django.contrib import admin
from .models import Account, Entry, Distribution, PrintsDistribution

class DistributionInlineAdmin(admin.TabularInline):
    model = Distribution

class EntryAdmin(admin.ModelAdmin):
    inlines = [DistributionInlineAdmin]


admin.site.register(Account)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Distribution)
admin.site.register(PrintsDistribution)

