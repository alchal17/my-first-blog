# Generated by Django 2.2.18 on 2021-12-04 00:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20211126_0326'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rating',
            options={'ordering': ['post_id']},
        ),
    ]
