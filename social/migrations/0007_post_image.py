# Generated by Django 4.0.5 on 2022-06-05 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0006_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/post_photos'),
        ),
    ]
