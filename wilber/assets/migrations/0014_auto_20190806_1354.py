# Generated by Django 2.2.3 on 2019-08-06 13:54

import assets.models
import assets.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0013_auto_20190709_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='category',
            field=models.CharField(choices=[('brushes', 'Brush'), ('patterns', 'Pattern'), ('gradients', 'Gradient'), ('palettes', 'Palette'), ('plug-ins', 'Plug-in')], max_length=9),
        ),
        migrations.AlterField(
            model_name='asset',
            name='description',
            field=models.TextField(max_length=3000),
        ),
        migrations.AlterField(
            model_name='asset',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=assets.models.get_file_path, validators=[assets.validators.FileValidator(max_size=10485760)]),
        ),
        migrations.AlterField(
            model_name='asset',
            name='image',
            field=models.ImageField(blank=True, default='images/none/no-img.jpg', null=True, upload_to=assets.models.get_image_path, validators=[assets.validators.FileValidator(max_size=10485760)]),
        ),
    ]