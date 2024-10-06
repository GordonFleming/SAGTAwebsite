from django.db import models
from django.contrib.auth.models import User

# Validation
TITLES = {
    "mr": "Mr",
    "mrs": "Mrs",
    "miss": "Miss",
    "ms": "Ms",
    "none": "None"
}
SADC_CHOICES = {
    "south_africa": "South Africa",
    "angola": "Angola",
    "botswana": "Botswana",
    "comoros": "Comoros",
    "democratic_republic_of_the_congo": "Democratic Republic of the Congo",
    "eswatini": "Eswatini",
    "lesotho": "Lesotho",
    "madagascar": "Madagascar",
    "malawi": "Malawi",
    "mauritius": "Mauritius",
    "mozambique": "Mozambique",
    "namibia": "Namibia",
    "seychelles": "Seychelles",
    "tanzania": "Tanzania",
    "zambia": "Zambia",
    "zimbabwe": "Zimbabwe"
}
MEMBERSHIP_CHOICES = {
    "individual": "Individual, SAGTA / AAG Joint Membership R480 / 1 year",
    "retired_teachers": "Retired teachers, SAGTA / AAG Joint Membership R240 / 1 year",
    "student_teachers": "Student teachers, SAGTA / AAG Joint Membership R240 / 1 year",
    "corporate_institutional": "Corporate Institutional Membership (max. 5 staff members) R2200 / 1 year"
}


# Create your models here.

class Member(models.Model):
    # One to one relationship with user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Members title
    title = models.CharField(verbose_name='title', max_length=4, choices=TITLES)
    # Name of your School/Tertiary Institution/Organisation
    school = models.CharField(verbose_name='school', max_length=255)
    #Position/Job Title
    position = models.CharField(verbose_name='position', max_length=255)
    # SADC Country of Residence
    country = models.CharField(verbose_name='SADC Country', max_length=255, choices=SADC_CHOICES)
    # secondary email, nullable
    secondary_email = models.CharField(verbose_name='secondary_email', max_length=255, null=True, blank=True)
    # Cell of organisation
    cell_org = models.CharField(verbose_name='cell', max_length=255)
    # Personal cell
    cell = models.CharField(verbose_name='cell', max_length=255, null=True, blank=True)
    # Website url of org
    website = models.CharField(verbose_name='website', max_length=255, null=True, blank=True)
    # Postal Mailing Address of Organisation
    address = models.CharField(verbose_name='address', max_length=255)
    # SACE
    sace = models.CharField(verbose_name='sace', max_length=255, null=True, blank=True)
    # Membership type
    membership_type = models.CharField(verbose_name='membership_type', max_length=255, choices=MEMBERSHIP_CHOICES)

# Reference: https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#extending-the-existing-user-model
# and https://docs.wagtail.org/en/stable/advanced_topics/customisation/custom_user_models.html#