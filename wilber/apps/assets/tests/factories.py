from random import randint

from django.conf import settings
from factory import Iterator
from factory import LazyAttribute
from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.django import FileField
from faker import Factory as FakerFactory
from pytz import timezone

from apps.assets.models import Asset
from apps.assets.models import Like
from apps.users.tests.factories import UserFactory

faker = FakerFactory.create()


class AssetFactory(DjangoModelFactory):
    class Meta:
        model = Asset

    # created = CreationDateTimeField We do not support this field type
    # modified = ModificationDateTimeField We do not support this field type
    owner = SubFactory(UserFactory)
    category = Iterator(Asset.CATEGORIES, getter=lambda x: x[0])
    name = LazyAttribute(lambda x: faker.text(max_nb_chars=100))
    # slug = AutoSlugField We do not support this field type
    description = LazyAttribute(
        lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True)
    )
    # source = URLField We do not support this field type
    source = "http://www.wilber.social"
    file = FileField(filename="file.xlsx")
    filesize = LazyAttribute(lambda o: randint(1, 100))
    # image = ProcessedImageField We do not support this field type
    # num_likes = PositiveIntegerField We do not support this field type
    # num_downloads = PositiveIntegerField We do not support this field type
    # num_views = PositiveIntegerField We do not support this field type
    created_at = LazyAttribute(
        lambda x: faker.date_time_between(
            start_date="-1y",
            end_date="now",
            tzinfo=timezone(settings.TIME_ZONE),
        )
    )
    updated_at = LazyAttribute(
        lambda x: faker.date_time_between(
            start_date="-1y",
            end_date="now",
            tzinfo=timezone(settings.TIME_ZONE),
        )
    )


class LikeFactory(DjangoModelFactory):
    class Meta:
        model = Like

    user = SubFactory(UserFactory)
    asset = SubFactory(AssetFactory)
    timestamp = LazyAttribute(
        lambda x: faker.date_time_between(
            start_date="-1y",
            end_date="now",
            tzinfo=timezone(settings.TIME_ZONE),
        )
    )
