from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated


from .models import Asset, Brush, Pattern


# Serializers define the API representation.
class AssetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Asset
        fields = ('type', 'name', 'description', 'image', 'file')

# ViewSets define the view behavior.
class AssetViewSet(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

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
