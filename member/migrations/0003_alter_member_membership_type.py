# Generated by Django 5.1.2 on 2024-12-11 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_alter_member_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='membership_type',
            field=models.CharField(choices=[('individual', 'Individual, SAGTA / AAG Joint Membership R500 / 1 year'), ('retired_teachers', 'Retired teachers, SAGTA / AAG Joint Membership R250 / 1 year'), ('student_teachers', 'Student teachers, SAGTA / AAG Joint Membership R250 / 1 year'), ('corporate_institutional', 'Corporate Institutional Membership (max. 5 staff members) R2300 / 1 year')], max_length=255, verbose_name='membership_type'),
        ),
    ]