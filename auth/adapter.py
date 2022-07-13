from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError
import os
from dotenv import load_dotenv

load_dotenv()

import gspread
from django.contrib.auth.models import Group

SHEET_ID = os.environ.get('SHEET_ID')
cred = {
  "type": "service_account",
  "project_id": os.environ.get('PROJECT_ID'),
  "private_key_id": os.environ.get('PRIVATE_KEY_ID'),
  "private_key": os.environ.get('PRIVATE_KEY'),
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
 
class RestrictEmailAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        member_email_check = sht.find(email)
        if not member_email_check:
            raise ValidationError('You are restricted from registering.\
                                Please contact us if you are a member.')
        return email