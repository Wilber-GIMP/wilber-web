# Generated by Django 2.2 on 2019-04-18 20:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assets', '0006_remove_asset_type2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='description',
            field=models.CharField(max_length=1000),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked', to='assets.Asset')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='asset',
            name='likes',
            field=models.ManyToManyField(related_name='liked', through='assets.Like', to=settings.AUTH_USER_MODEL),
        ),
    ]