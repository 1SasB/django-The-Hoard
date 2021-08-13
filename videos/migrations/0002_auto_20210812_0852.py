# Generated by Django 3.2.5 on 2021-08-12 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='path',
            field=models.FileField(upload_to='videos/', verbose_name='PATH'),
        ),
        migrations.AlterField(
            model_name='video',
            name='thumbnail',
            field=models.FileField(blank=True, upload_to='thumbnails/'),
        ),
    ]
