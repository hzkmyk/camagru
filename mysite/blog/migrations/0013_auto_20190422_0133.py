# Generated by Django 2.1.7 on 2019-04-22 01:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20190422_0131'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Commen',
            new_name='Comment',
        ),
    ]