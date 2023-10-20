# Generated by Django 4.2.5 on 2023-10-19 12:56

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_homepage_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='carousel_images',
            field=wagtail.fields.StreamField([('carousel_image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock())]))], blank=True, use_json_field=True),
        ),
    ]