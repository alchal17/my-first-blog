# Generated by Django 2.2.18 on 2021-12-04 00:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20211204_0222'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rating',
            options={'ordering': ('value',)},
        ),
    ]
