# Generated by Django 2.2.3 on 2019-07-26 14:02

from django.db import migrations


from django.db import transaction

@transaction.atomic
def save_all(apps, schema_editor):
    # We can't import the Image model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    User = apps.get_model('users', 'User')
    for user in User.objects.all():
        user.save()
        print(user)

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190726_1401'),
    ]

    operations = [
        migrations.RunPython(save_all),
    ]
