from django.contrib import admin
from member.admin import CustomUserAdmin
from django.contrib.auth.models import User
from .models import Payment, UserWallet

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    can_delete = True
    readonly_fields = ('verified', 'ref', 'created_at')
    fields = ('amount', 'email', 'verified', 'ref', 'created_at')
    ordering = ('-created_at',)
    max_num = 10  # Limits the number of payments shown
    show_change_link = True

class UserWalletInline(admin.StackedInline):
    model = UserWallet
    can_delete = False
    verbose_name_plural = "wallet"
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'email', 'verified', 'created_at', 'ref')
    list_filter = ('verified', 'created_at', 'user')
    search_fields = ('user__username', 'user__email', 'email', 'ref')
    readonly_fields = ('verified', 'ref', 'created_at')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'currency', 'balance', 'created_at', 'updated_at')
    list_filter = ('currency', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)

class ExtendedCustomUserAdmin(CustomUserAdmin):
    inlines = CustomUserAdmin.inlines + [UserWalletInline, PaymentInline]

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, ExtendedCustomUserAdmin)