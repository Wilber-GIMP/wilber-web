# Generated by Django 2.2.3 on 2019-11-10 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0018_auto_20191019_2151'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='num_shares',
            new_name='num_views',
        ),
    ]