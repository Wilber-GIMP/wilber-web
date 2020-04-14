import django_filters
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.assets.models import Asset
from apps.assets.models import Like
from apps.users.models import User
from apps.users.models import UserProfile


class MultiSerializerViewSetMixin(object):
    def get_serializer_class(self):
        """
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:

        class MyViewSet(MultiSerializerViewSetMixin, ViewSet):
            serializer_class = MyDefaultSerializer
            serializer_action_classes = {
               'list': MyListSerializer,
               'my_action': MyActionSerializer,
            }

            @action
            def my_action:
                ...

        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class, DefaultSerializer.

        """
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(
                MultiSerializerViewSetMixin, self
            ).get_serializer_class()


class AssetListSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    folder = serializers.ReadOnlyField()
    username = serializers.CharField(source="owner", read_only=True)
    search_fields = ["name", "description"]
    image_thumbnail = serializers.ImageField(read_only=True)
    is_liked = serializers.SerializerMethodField("_is_liked")

    def _is_liked(self, obj):
        request = self.context.get("request")
        if request:
            return obj.is_liked(request._user)
        return None

    class Meta:
        model = Asset

        fields = [
            "id",
            "url",
            "username",
            "category",
            "name",
            "image",
            "image_thumbnail",
            "file",
            "folder",
            "num_likes",
            "is_liked",
        ]


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserProfile
        fields = "__all__"


class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    profile = UserProfileSerializer(read_only=True)
    assets = AssetListSerializer(many=True, read_only=True)

    class Meta:
        model = User
        exclude = ["password", "user_permissions"]


class UserInlineSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        exclude = ["password", "user_permissions"]


class UserListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["id", "url", "absolute_url", "name", "username"]


class UserViewSet(MultiSerializerViewSetMixin, viewsets.ModelViewSet):
    serializer_action_classes = {"list": UserListSerializer}
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="user-detail"
    )
    username = serializers.CharField(source="user", read_only=True)
    name = serializers.CharField(source="user.get_full_name", read_only=True)
    photo = serializers.CharField(source="user.profile.photo", read_only=True)

    class Meta:
        model = Like

        fields = ("user", "username", "name", "photo")


class AssetSerializer(serializers.HyperlinkedModelSerializer):
    owner = UserInlineSerializer(read_only=True)
    id = serializers.ReadOnlyField()
    folder = serializers.ReadOnlyField()
    filesize = serializers.ReadOnlyField()
    num_likes = serializers.ReadOnlyField()
    num_downloads = serializers.ReadOnlyField()
    num_shares = serializers.ReadOnlyField()

    likes = LikeSerializer(source="liked", many=True, read_only=True)

    current_user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    is_liked = serializers.SerializerMethodField("_is_liked")

    def _is_liked(self, obj):
        request = self.context.get("request")
        if request:
            return obj.is_liked(request._user)
        return None

    class Meta:
        model = Asset
        fields = "__all__"


class AssetFilter(filters.FilterSet):
    created_gte = django_filters.DateTimeFilter(
        field_name="created", lookup_expr="gte"
    )
    modified_gte = django_filters.DateTimeFilter(
        field_name="modified", lookup_expr="gte"
    )

    created_lte = django_filters.DateTimeFilter(
        field_name="created", lookup_expr="lte"
    )
    modified_lte = django_filters.DateTimeFilter(
        field_name="modified", lookup_expr="lte"
    )

    class Meta:
        model = Asset
        fields = [
            "name",
            "category",
            "description",
            "created",
            "created_gte",
            "created_lte",
            "modified",
            "modified_gte",
            "modified_lte",
            "owner__username",
            "owner__name",
        ]


class AssetViewSet(MultiSerializerViewSetMixin, viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = [
        "name",
        "category",
        "description",
        "created",
        "modified",
        "owner__username",
        "owner__name",
    ]
    filter_class = AssetFilter
    search_fields = [
        "name",
        "category",
        "description",
        "owner__username",
        "owner__name",
    ]
    # search_fields = ['name', 'owner__username']
    serializer_action_classes = {"list": AssetListSerializer}

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset2(self):
        """
        Restrict the donwloads to a single asset category
        """
        queryset = Asset.objects.all()
        category = self.request.query_params.get("category", None)
        if category is not None:
            queryset = queryset.filter(category=category)

        return queryset

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_name="like",
    )
    def like(self, request, pk=None):
        asset = self.get_object()
        user = request.user
        like, created = asset.do_like(user)
        asset.refresh_from_db()
        if created:
            status = "liked by %s" % user
        else:
            status = "already liked by %s at %s" % (user, like.timestamp)
        return Response({"status": status, "likes": asset.num_likes})

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        asset = self.get_object()
        user = request.user
        unliked = asset.unlike(user)
        asset.refresh_from_db()

        if unliked:
            status = "unliked"
        else:
            status = "this asset was not liked by this user"

        return Response({"status": status, "likes": asset.num_likes})

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_name="like",
    )
    def toggle_like(self, request, pk=None):
        asset = self.get_object()
        user = request.user
        toggle = asset.toggle_like(user)
        asset.refresh_from_db()
        status = toggle

        return Response(
            {"status": status, "likes": asset.num_likes, "liked": toggle}
        )

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        asset = self.get_object()
        user = request.user
        asset.download()
        asset.refresh_from_db()

        if user:
            status = "Downloaded by user:%s" % (user)
        else:
            status = "Downloaded by anon"

        return Response({"status": status, "downloads": asset.num_downloads})
