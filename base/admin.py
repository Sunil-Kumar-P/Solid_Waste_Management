# admin.py

from django.contrib import admin
from .models import User, ClientRequest, CollectorReport, Payment


class CollectorReportInline(admin.TabularInline):
    model = CollectorReport

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'mobile_number')

class ClientRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'type_of_waste', 'timestamp')


class CollectorReportAdmin(admin.ModelAdmin):
    list_display = ('collector', 'client_request', 'material', 'quantity', 'detail', 'timestamp')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'timestamp')

admin.site.register(User, UserAdmin)
admin.site.register(ClientRequest, ClientRequestAdmin)
admin.site.register(CollectorReport, CollectorReportAdmin)
admin.site.register(Payment, PaymentAdmin)
