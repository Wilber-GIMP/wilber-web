# Generated by Django 2.2 on 2019-05-10 00:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0011_delete_assettype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='type',
            new_name='category',
        ),
    ]