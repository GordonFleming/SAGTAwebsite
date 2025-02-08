from django import forms
from member.models import TITLES, SADC_CHOICES, MEMBERSHIP_CHOICES
from member.models import Member
from django.db import transaction
from datetime import datetime
from auth.adapter import append_row

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name', 
                                 widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name = forms.CharField(max_length=30, label='Last Name',
                                 widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    
    @transaction.atomic
    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        # Now, create and save the associated Member instance
        member = Member(
            user=user,  # Associate the new member with the newly created user
            title=self.cleaned_data.get('title'),
            school=self.cleaned_data.get('school'),
            position=self.cleaned_data.get('position'),
            country=self.cleaned_data.get('country'),
            secondary_email=self.cleaned_data.get('secondary_email'),
            cell_org=self.cleaned_data.get('cell_org'),
            cell=self.cleaned_data.get('cell'),
            website=self.cleaned_data.get('website'),
            address=self.cleaned_data.get('address'),
            sace=self.cleaned_data.get('sace'),
            membership_type=self.cleaned_data.get('membership_type'),
        )
        member.save()  # Save the Member object to the database

        # TODO: optional save to Google Sheet with gspread
        # refer to this: https://stackoverflow.com/questions/67082749/append-a-new-row-to-the-end-of-sheets-using-gspread
        # Save to Google Sheet
        try:
            # Prepare row data
            row_data = [
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Timestamp
                '',
                '',
                '',
                self.cleaned_data.get('title'),
                user.last_name,
                user.first_name,
                self.cleaned_data.get('school'),
                self.cleaned_data.get('position'),
                self.cleaned_data.get('country'),
                user.email,
                self.cleaned_data.get('secondary_email') or '',
                self.cleaned_data.get('cell_org'),
                self.cleaned_data.get('cell') or '',
                self.cleaned_data.get('website') or '',
                self.cleaned_data.get('address'),
                self.cleaned_data.get('sace') or '',
                self.cleaned_data.get('membership_type')
            ]
            
            # Append the new row
            append_row(row_data)
            
        except Exception as e:
            # Log the error but don't stop the signup process
            print(f"Error saving to Google Sheet: {str(e)}")
            # You might want to add proper logging here
            pass


        return user  # Return the user instance as required by Allauth

class CustomSignupForm(SignupForm):
    required_css_class = 'required'
    """
    Custom signup form for collecting additional fields for the Member model during the registration process.
    """
    title = forms.ChoiceField(choices=TITLES, label='Title', required=True)
    school = forms.CharField(max_length=100, label='Name of your School / Tertiary Institution / Organisation', required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Enter name here'}))
    position = forms.CharField(max_length=100, label='Position/Job Title', required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Your position'}))
    country = forms.ChoiceField(choices=SADC_CHOICES, label='SADC Country', required=True)
    secondary_email = forms.EmailField(max_length=100, label='Secondary Email', required=False,
                                       widget=forms.EmailInput(attrs={'placeholder': 'Optional secondary email'}))
    cell_org = forms.CharField(max_length=100, label='Telephone Number of Organisation', required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Please include country dialing code'}))
    cell = forms.CharField(max_length=15, label='Cellphone/Mobile phone number (optional)', required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}))
    website = forms.URLField(max_length=100, label='Website/URL of your organisation', required=False,
                             widget=forms.URLInput(attrs={'placeholder': 'Your website (optional)'}))
    address = forms.CharField(max_length=200, label="Postal Mailing Address of Organisation",
                                help_text=(
                                "Please include postal code. Your SAGTA membership includes a membership to AAG. "
                                "For their auditing purposes, they require a postal address for all members."
                                ),
                                widget=forms.Textarea(attrs={"rows": 3}), required=True,)
    sace = forms.CharField(max_length=50, label='SACE Number', required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Optional SACE number'}))
    membership_type = forms.ChoiceField(choices=MEMBERSHIP_CHOICES, label='Membership Type', required=True)

    class Meta:
        fields = ['title', 'school', 'position', 'country', 'secondary_email', 'cell_org', 'cell', 'website', 'address', 'sace', 'membership_type']
