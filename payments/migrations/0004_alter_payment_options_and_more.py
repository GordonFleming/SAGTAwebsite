# Generated by Django 5.0.9 on 2024-10-18 16:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_alter_userwallet_currency'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ('-created_at',)},
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='date_created',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='userwallet',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='userwallet',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
