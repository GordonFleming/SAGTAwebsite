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

# Open a sheet from a spreadsheet in one go
sheet = gc.open_by_key(SHEET_ID)
sht = sheet.sheet1

# Email column is column 4
member_email_list = sht.col_values(4)
 
class RestrictEmailAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        RestrictedList = member_email_list
        if email not in RestrictedList:
            raise ValidationError('You are restricted from registering.\
                                Please contact us if you are a member.')
        return email