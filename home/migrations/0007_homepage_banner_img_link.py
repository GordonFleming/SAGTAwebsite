# Generated by Django 3.2.3 on 2021-06-22 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_remove_homepage_banner_cta'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='banner_img_link',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
