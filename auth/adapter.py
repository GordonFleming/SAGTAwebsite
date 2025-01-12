from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError
import os
from django.urls import reverse
import gspread
from django.contrib.auth.models import Group, User
from payments.models import UserWallet, Payment
from datetime import timedelta
from django.utils import timezone
from dotenv import load_dotenv
load_dotenv()

SHEET_ID = os.environ.get('SHEET_ID')
private = os.environ.get('PRIVATE_KEY')
cred = {
    "type": "service_account",
    "project_id": os.environ.get('PROJECT_ID'),
    "private_key_id": os.environ.get('PRIVATE_KEY_ID'),
    "private_key": f'-----BEGIN PRIVATE KEY-----\nM{private}g+F7\nqhol/Qn+AamqGfsmmsq6NWgIYEN1uX7W1OjuqHp0QqeZ77n0vsJwIeYwh3xU/XIs\nNmHhnussNbgUmDIjRe7HNOvo70S0J242yEzPtcE7oErWPwOg58LVm0j14tPLRbXA\nOqmwPF5NboMeWkm0dMVn/FIoqRZ7NR77s3gWQFKYiP+qKIqnqCQfkMFfGASmHBQ9\nI8XOw4PCbPC2kc61mo3nRUuuY7A7H1nuNsDYLFnwShJ9km8Nb+I/kjPPtSAzlRm4\nu1H62LH6IM8+RlKRvCIjvooXUR4Ft1oY57GygNGusbnB5Kj16+o4eSWzfl9FRP88\ncTmhF7CBAgMBAAECggEACh3Naez62kbczWtvJVBr98MVam7wzXKUpLzMsVfbVfsE\nTrEU8KRPYk0Iz0WPPbFtPVbvHjAdTr8udXy4B7eOGiEj0mTG0nwF02LXCztppra4\n+3Cp7zQJ/flKOn3egpL2kJSx0w6CZubyVGUDE1YNTYbvwZv95FjButPDIZopcjWu\n3O2gDmoC/RVvntH3nQmObrJ3hH/cHxJBhH+k+FUIXL7ZkBwVQsh75Q9MVugBRmhG\netaVAqZ7JSXd3NEJ0f/kqIAZMIwhz9XJ1eHS0AIjiMH0sxhXRhUYuUAFPsBo5R1P\n0+M7eXT8+Uy3LPy8bBruSH9E/aNjGrJsOu2Je1TTQwKBgQDsHFvuoKbJSib9GX97\nu9Cd4rJjS4lJwWnHSS/CQi8AI1TkKEZ2eSnkOlSSHk70D1jo94cka9JCdMrXGhnR\nu9Y7xC49CkWVEzDQCK6oaiI6V2VPmeByYaN1EfBP18MBv5ftAa1jyrH+BzQl6mJ7\nAoc6AYnCr66SgGSyoq1GzWhzEwKBgQDLMlJoUkKBM6oc1DSM/+rtW+Xp9urw9Ctf\nYx7epxnjNTX/6N5GAMI9WgMrm3IxmB0vJ8XYQ/O6DyV8c6MW1CDZlAiKbsO2WCXR\nkuWwFTpniPqf0YkKE83wTmZFR0lrc8MJZyfw9Jq+nn1CyZIKdfRq2FLJOGvoB4zC\nzXbWYDpsmwKBgQCv/veb6U5Jjqd/VAlN3xLDDZ8xGrYML0q8zNX3tEO6k5uMsmTL\nnMdYIw61GDh7/hClHxUyVdiVxt8H9aG3T4+CX1qkD0sMsxBYkZA3Y11+JXUUH7xJ\nJnSkKCn8KfVnETya4vwu/YEtvIrnlE2yKZFI8KqSX0f+Vgw5h78nnqcz1wKBgQDE\n78rK7R8j1g0Dz+/20HrC/hSBhB0E18HJu2nJ5i7C9WmW0/3J3yZjDACSnSA6TPHM\nKEIqbwGjzNZKHlFs6L/F4SG9+ciZzCkrS7JtzMVEX5B4oT6uk68/Pt0EPCk+iX34\neRBPCuOH6FgDCRYQKW5wt6TU/WgoBFk63KRW9gDqDQKBgQDXLH7b06gDt/L38Qem\ns1M+B8cgh6akkpf85xTPBADGCs0RFQRkzWjHqoHNZl38358ZuE5+nOymGPZU9ye3\nkWrw/jW6kz15tCvnQqV2f7N/kAycDgQHF2286rotK60rkd6eJy6BNUvKqGhUwSYS\nj3XW/f22AfKZmcPt+89XbuyQ+Q==\n-----END PRIVATE KEY-----\n',
    "client_email": os.environ.get('CLIENT_EMAIL'),
    "client_id": os.environ.get('CLIENT_ID'),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/387800386672-compute%40developer.gserviceaccount.com"
}

gc = gspread.service_account_from_dict(cred)

sheet = gc.open_by_key(SHEET_ID)
sht = sheet.sheet1

def is_valid_member(email):
    member_email_check = sht.find(email.lower())
    if not member_email_check:
        return False
    return True
 
class CustomEmailPaymentAdapter(DefaultAccountAdapter):
    def _should_redirect_to_payment(self, request):
        """Helper method to determine if user should be redirected to payment"""
        user = request.user

        is_member = user.groups.filter(name='Members').exists()
        if is_member:
            return False
        
        # Ensure the UserWallet exists, create if not
        wallet, created = UserWallet.objects.get_or_create(user=user)
        
        # Check if user is legacy member or has positive balance
        eft_legacy_member = is_valid_member(user.email)
        paid_member = wallet.balance > 0
        
        return not (eft_legacy_member or paid_member)

    def _get_redirect_url(self, request):
        """Helper method to get the appropriate redirect URL"""
        # If user shouldn't be redirected to payment, send them to prep-share
        if not self._should_redirect_to_payment(request):
            return '/'
            
        # Check if we're already on the payment page to prevent infinite loops
        current_path = request.path
        payment_path = reverse('initiate_payment')
        
        # If we're already on the payment page, redirect to home
        if current_path == payment_path:
            return '/'
            
        # Otherwise, redirect to payment
        return payment_path

    def get_login_redirect_url(self, request):
        return self._get_redirect_url(request)
    
    def get_signup_redirect_url(self, request):
        return self._get_redirect_url(request)
    
    # Deprecated: as checks need to be on payment & Gsheet for manual process (EFT)

    # def clean_email(self, email):
    #     # Paystack check
    #     if not is_valid_member(email):
    #         raise ValidationError('You are restricted from registering.\
    #                             Please contact us if you are a member.')
    #     return email

def validate_users():
    # Members from google sheet (Paid via EFT directly)
    all_members = set(sht.col_values(7))
    
    validated_members = []
    invalidated_members = []
    users = User.objects.all()

    for user in users:
        try:
            latest_payment = Payment.objects.filter(verified=True).order_by('-created_at').first()
        except IndexError:  # Handle case where no payments exist
            latest_payment = None 

        user_wallet, created = UserWallet.objects.get_or_create(user=user)
        group = Group.objects.get(name='Members')

        # Conditions
        already_member = user.groups.filter(name='Members').exists()
        sheet_member = user.email.lower() in all_members
        
        under_year = latest_payment and latest_payment.created_at > timezone.now() - timedelta(days=365)
        
        has_balance = user_wallet.balance > 0

        if not already_member and (sheet_member or (under_year and has_balance)):
            validated_members.append(user.email)
            user.groups.add(group)
            user.is_active = True
        elif already_member and not (sheet_member or (under_year and has_balance)):
            invalidated_members.append(user.email)
            user.groups.remove(group)
            user_wallet.balance = 0
            user_wallet.save()
        
        user.save()


    return  { 
            "Users validated": validated_members,
            "count_val": len(validated_members), 
            "Users invalidated": invalidated_members,
            "count_inv": len(invalidated_members),
        }
