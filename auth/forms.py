from django import forms
from member.models import TITLES, SADC_CHOICES, MEMBERSHIP_CHOICES
from member.models import Member
from django.db import transaction

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

        print(request)
        print(self.cleaned_data)
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

        return user  # Return the user instance as required by Allauth

class CustomSignupForm(SignupForm):
    required_css_class = 'required'
    """
    Custom signup form for collecting additional fields for the Member model during the registration process.
    """
    title = forms.ChoiceField(choices=TITLES, label='Title', required=True)
    school = forms.CharField(max_length=100, label='School', required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Type your school name'}))
    position = forms.CharField(max_length=100, label='Position', required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Your position in school'}))
    country = forms.ChoiceField(choices=SADC_CHOICES, label='SADC Country', required=True)
    secondary_email = forms.EmailField(max_length=100, label='Secondary Email', required=False,
                                       widget=forms.EmailInput(attrs={'placeholder': 'Optional secondary email'}))
    cell_org = forms.CharField(max_length=100, label='Cell Organization', required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Type your organization'}))
    cell = forms.CharField(max_length=15, label='Cell Number', required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}))
    website = forms.URLField(max_length=100, label='Website', required=False,
                             widget=forms.URLInput(attrs={'placeholder': 'Your website (optional)'}))
    address = forms.CharField(max_length=200, label='Address', required=True,
                              widget=forms.TextInput(attrs={'placeholder': 'Enter your address'}))
    sace = forms.CharField(max_length=50, label='SACE Number', required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Optional SACE number'}))
    membership_type = forms.ChoiceField(choices=MEMBERSHIP_CHOICES, label='Membership Type', required=True)

    class Meta:
        fields = ['title', 'school', 'position', 'country', 'secondary_email', 'cell_org', 'cell', 'website', 'address', 'sace', 'membership_type']
