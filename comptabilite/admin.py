from django.contrib import admin

from .models import Account, Entry, Distribution, PrintsDistribution

admin.site.register(Account)
admin.site.register(Entry)
admin.site.register(Distribution)
admin.site.register(PrintsDistribution)

