# Generated by Django 2.2 on 2019-04-18 20:34

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assets', '0008_auto_20190418_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='timestamp',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('user', 'asset')},
        ),
    ]