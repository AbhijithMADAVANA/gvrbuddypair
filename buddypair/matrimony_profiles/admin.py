from django.contrib import admin
from .models import InterestRequest, Shortlist,MatrimonyFriendship
# Register your models here
# admin.site.register(InterestRequest)
admin.site.register(Shortlist)
admin.site.register(MatrimonyFriendship)

from django.contrib import admin
from .models import InterestRequest

@admin.register(InterestRequest)
class InterestRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'created_at')

