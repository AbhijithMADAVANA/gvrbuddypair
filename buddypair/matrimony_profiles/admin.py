from django.contrib import admin
from .models import InterestRequest, Shortlist,MatrimonyFriendship,MatrimonyProfileViewCounter
# Register your models here
# admin.site.register(InterestRequest)
admin.site.register(Shortlist)
admin.site.register(MatrimonyFriendship)
admin.site.register(MatrimonyProfileViewCounter)


@admin.register(InterestRequest)
class InterestRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'created_at')

