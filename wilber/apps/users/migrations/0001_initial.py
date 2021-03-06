# Generated by Django 3.0.5 on 2020-04-13 20:53
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = [("auth", "0011_update_proxy_permissions")]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "password",
                    models.CharField(max_length=128, verbose_name="password"),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 15 characters or fewer. Letters, \\ numbers and @/./+/-/_ characters",
                        max_length=15,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        max_length=127, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(max_length=127, verbose_name="last name"),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="full name",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        max_length=255,
                        verbose_name="email address",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="date joined",
                    ),
                ),
                (
                    "is_trusty",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether this user has confirmed his account.",
                        verbose_name="trusty",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={"verbose_name": "user", "verbose_name_plural": "users"},
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        default="profiles/none/no-image-profile.png",
                        max_length=255,
                        null=True,
                        upload_to="profiles",
                        verbose_name="Profile Picture",
                    ),
                ),
                (
                    "phone",
                    models.CharField(blank=True, default="", max_length=20),
                ),
                ("bio", models.TextField(blank=True, default="")),
                (
                    "organization",
                    models.CharField(blank=True, default="", max_length=100),
                ),
                ("website", models.URLField(blank=True, default="")),
                (
                    "facebook",
                    models.CharField(blank=True, default="", max_length=50),
                ),
                (
                    "instagram",
                    models.CharField(blank=True, default="", max_length=50),
                ),
                ("birthday", models.DateField(blank=True, null=True)),
                (
                    "city",
                    models.CharField(blank=True, default="", max_length=100),
                ),
                (
                    "country",
                    models.CharField(blank=True, default="", max_length=100),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-modified", "-created"),
                "get_latest_by": "modified",
                "abstract": False,
            },
        ),
    ]
