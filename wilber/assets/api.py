from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated


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






class AssetSerializer(serializers.HyperlinkedModelSerializer):
    owner = UserInlineSerializer(read_only=True)
    id = serializers.ReadOnlyField()
    type = serializers.StringRelatedField(many=False)
    #'image_count' = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Asset
        
        fields = '__all__'


class AssetListSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField(source='owner', read_only=True)
    type = serializers.StringRelatedField(many=False)
    folder = serializers.ReadOnlyField()
    
    class Meta:
        model = Asset
    
        fields = ['id', 'username', 'type', 'folder', ]
        fields = '__all__'


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
        type = self.request.query_params.get('type', None)
        if type is not None:
            queryset = queryset.filter(type=type)
        return queryset

