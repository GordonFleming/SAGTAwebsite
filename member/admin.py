from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from .models import Member
from payments.models import UserWallet

class MemberInline(admin.StackedInline):
    model = Member
    can_delete = False
    verbose_name_plural = "Member"

class CustomUserAdmin(BaseUserAdmin):
    inlines = [MemberInline]

# Unregister the default User admin and register the custom UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)

class MemberResource(resources.ModelResource):
    # Define custom fields for export
    email = fields.Field(attribute='user__email', column_name='Email')
    first_name = fields.Field(attribute='user__first_name', column_name='First Name')
    last_name = fields.Field(attribute='user__last_name', column_name='Last Name')
    wallet_balance = fields.Field(column_name='Wallet Balance')

    class Meta:
        model = Member
        fields = ('id', 'email', 'first_name', 'last_name', 'school', 'position', 'country', 
                  'secondary_email', 'cell_org', 'cell', 'website', 'address', 'sace', 'membership_type', 'wallet_balance')
        export_order = ('id', 'email', 'first_name', 'last_name', 'school', 'position', 'country', 
                        'secondary_email', 'cell_org', 'cell', 'website', 'address', 'sace', 'membership_type', 'wallet_balance')

    def dehydrate_wallet_balance(self, member):
        try:
            wallet = UserWallet.objects.get(user=member.user)
            return f"{wallet.currency} {wallet.balance}"
        except UserWallet.DoesNotExist:
            return '-'

@admin.register(Member)
class MemberAdmin(ImportExportModelAdmin):
    resource_class = MemberResource  # Use the custom resource class
    list_display = ('user__email', 'user__first_name', 'user__last_name', 'school', 
                    'membership_type', 'get_wallet_balance')
    list_filter = ('country', 'membership_type')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    
    def get_wallet_balance(self, obj):
        try:
            wallet = UserWallet.objects.get(user=obj.user)
            return f"{wallet.currency} {wallet.balance}"
        except UserWallet.DoesNotExist:
            return '-'
    get_wallet_balance.short_description = 'Wallet Balance'