from django.contrib import admin
from .models import Payment, UserWallet

class PaymentAdmin(admin.ModelAdmin):
	list_display = ["id", "ref", 'amount', "verified", "created_at"]


admin.site.register(Payment, PaymentAdmin)
admin.site.register(UserWallet)