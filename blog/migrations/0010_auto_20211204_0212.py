# Generated by Django 2.2.18 on 2021-12-04 00:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20211204_0211'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rating',
            options={'ordering': ['post']},
        ),
    ]