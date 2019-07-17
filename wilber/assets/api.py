from rest_framework import serializers, viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.fields import CurrentUserDefault
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import *
from users.models import User, UserProfile

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
            return super(MultiSerializerViewSetMixin, self).get_serializer_class()


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    assets = serializers.HyperlinkedRelatedField(many=True, view_name='asset-detail', read_only=True)

    class Meta:
        model = User
        exclude = ['password', 'user_permissions']

class UserInlineSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        exclude = ['password', 'user_permissions']

class UserListSerializer(serializers.HyperlinkedModelSerializer):
    #profile = UserProfileSerializer(read_only=True)
    #assets = serializers.HyperlinkedRelatedField(many=True, view_name='asset-detail', read_only=True)
    class Meta:
        model = User
        fields = ['id', 'url', 'name', 'username']



class UserViewSet(MultiSerializerViewSetMixin, viewsets.ModelViewSet):
    serializer_action_classes = {
        'list': UserListSerializer,
    }
    #permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer



class LikeSerializer(serializers.ModelSerializer):
    #view_name = 'like-detail'

    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')
    username = serializers.CharField(source='user', read_only=True)
    name = serializers.CharField(source='user.get_full_name', read_only=True)
    photo = serializers.CharField(source='user.profile.photo', read_only=True)
    #asset = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Like
        #fields = ('__all__')
        fields = ('user', 'username', 'name', 'photo')



class AssetSerializer(serializers.HyperlinkedModelSerializer):
    owner = UserInlineSerializer(read_only=True)
    id = serializers.ReadOnlyField()
    folder = serializers.ReadOnlyField()
    filesize = serializers.ReadOnlyField()
    num_likes = serializers.ReadOnlyField()
    num_downloads = serializers.ReadOnlyField()
    num_shares = serializers.ReadOnlyField()


    likes = LikeSerializer(source='liked', many=True, read_only=True)

    current_user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    is_liked = serializers.SerializerMethodField('_is_liked')

    def _is_liked(self, obj):
        request = self.context.get('request')
        if request:
            return obj.is_liked(request._user)
        return None


    class Meta:
        model = Asset
        fields = '__all__'


class AssetListSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    folder = serializers.ReadOnlyField()
    username = serializers.CharField(source='owner', read_only=True)

    is_liked = serializers.SerializerMethodField('_is_liked')

    def _is_liked(self, obj):
        request = self.context.get('request')
        if request:
            return obj.is_liked(request._user)
        return None


    class Meta:
        model = Asset

        fields = ['id', 'url', 'username', 'category', 'name', 'image', 'file', 'folder', 'num_likes', 'is_liked' ]


class AssetViewSet(MultiSerializerViewSetMixin, viewsets.ModelViewSet ):
    #permission_classes = (IsAuthenticated,)
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    serializer_action_classes = {
        'list': AssetListSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Asset.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        return queryset

    @action(detail=True, methods=['get',], permission_classes=[IsAuthenticated], url_name='like')
    def like(self, request, pk=None):
        asset = self.get_object()
        user = request.user
        like, created = asset.do_like(user)
        asset.refresh_from_db()

        if created:
            status = 'liked by %s' % user
        else:
            status = 'already liked by %s at %s' % (user, like.timestamp)

        return Response({'status':status, 'likes':asset.num_likes})



    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        asset = self.get_object()
        user = request.user

        unliked = asset.unlike(user)
        asset.refresh_from_db()

        if unliked:
            status = 'unliked'
        else:
            status = 'this asset was not liked by this user'

        return Response({'status':status, 'likes':asset.num_likes})

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        asset = self.get_object()
        user = request.user
        num_downloads = asset.download()
        asset.refresh_from_db()

        if user:
            status = 'Downloaded by user:%s' % (user)
        else:
            status = 'Downloaded by anon'

        return Response({'status':status, 'downloads':asset.num_downloads})



