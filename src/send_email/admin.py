from django.contrib import admin
from .models import MailingListMember

class MailingListMemberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_date')  # 表示するフィールド

admin.site.register(MailingListMember, MailingListMemberAdmin)
