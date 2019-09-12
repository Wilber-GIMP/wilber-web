# Generated by Django 2.2.3 on 2019-08-07 00:37

import assets.models
import assets.validators
from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0016_auto_20190806_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='file',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to=assets.models.get_file_path, validators=[assets.validators.FileValidator(max_size=10485760)]),
        ),
        migrations.AlterField(
            model_name='asset',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default='images/no-img.png', max_length=255, null=True, upload_to=assets.models.get_image_path, validators=[assets.validators.FileValidator(max_size=10485760)]),
        ),
    ]