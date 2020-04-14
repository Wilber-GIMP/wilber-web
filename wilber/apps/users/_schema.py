import graphene
from graphene_django.types import DjangoObjectType

from apps.users.models import User
from apps.users.models import UserProfile


class UserType(DjangoObjectType):
    class Meta:
        model = User


class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile


class Query(object):
    all_users = graphene.List(UserType)
    all_user_profiles = graphene.List(UserType)

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_all_user_profiles(self, info, **kwargs):
        return UserProfile.objects.all()
