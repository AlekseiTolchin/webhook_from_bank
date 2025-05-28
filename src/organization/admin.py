from django.contrib import admin

from .models import Organization, Payment, BalanceLog


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('inn', 'balance')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('operation_id', 'amount')


@admin.register(BalanceLog)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('organization', 'amount', 'new_balance', 'date')
