# Generated by Django 3.2.3 on 2021-06-22 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_homepage_banner_img_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='banner_img_link',
            field=models.CharField(max_length=400, null=True),
        ),
    ]
