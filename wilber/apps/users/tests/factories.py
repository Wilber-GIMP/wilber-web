from django.conf import settings
from factory import Iterator
from factory import LazyAttribute
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from pytz import timezone

from apps.users.models import User
from apps.users.models import UserProfile


faker = FakerFactory.create()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    password = LazyAttribute(lambda x: faker.text(max_nb_chars=128))
    last_login = LazyAttribute(
        lambda x: faker.date_time_between(
            start_date="-1y",
            end_date="now",
            tzinfo=timezone(settings.TIME_ZONE),
        )
    )
    is_superuser = Iterator([True, False])
    username = LazyAttribute(lambda x: faker.text(max_nb_chars=15))
    first_name = LazyAttribute(lambda x: faker.text(max_nb_chars=127))
    last_name = LazyAttribute(lambda x: faker.text(max_nb_chars=127))
    name = LazyAttribute(lambda x: faker.text(max_nb_chars=255))
    # email = EmailField We do not support this field type
    is_staff = Iterator([True, False])
    is_active = Iterator([True, False])
    date_joined = LazyAttribute(
        lambda x: faker.date_time_between(
            start_date="-1y",
            end_date="now",
            tzinfo=timezone(settings.TIME_ZONE),
        )
    )
    is_trusty = Iterator([True, False])


class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserProfile

    # created = CreationDateTimeField We do not support this field type
    # modified = ModificationDateTimeField We do not support this field type
    # user = OneToOneField We do not support this field type
    # photo = ImageField We do not support this field type
    phone = LazyAttribute(lambda x: faker.text(max_nb_chars=20))
    bio = LazyAttribute(
        lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True)
    )
    organization = LazyAttribute(lambda x: faker.text(max_nb_chars=100))
    # website = URLField We do not support this field type
    facebook = LazyAttribute(lambda x: faker.text(max_nb_chars=50))
    instagram = LazyAttribute(lambda x: faker.text(max_nb_chars=50))
    birthday = LazyAttribute(
        lambda x: faker.date_time_between(
            start_date="-1y",
            end_date="now",
            tzinfo=timezone(settings.TIME_ZONE),
        )
    )
    city = LazyAttribute(lambda x: faker.text(max_nb_chars=100))
    country = LazyAttribute(lambda x: faker.text(max_nb_chars=100))

    # user = SubFactory(UserFactory)
