from rest_framework import serializers, viewsets

from .models import Asset, Brush, Pattern


# Serializers define the API representation.
class AssetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Asset
        fields = ('name', 'description')

# ViewSets define the view behavior.
class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer



# Serializers define the API representation.
class BrushSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Asset
        fields = ('name', 'description')

# ViewSets define the view behavior.
class BrushViewSet(viewsets.ModelViewSet):
    queryset = Brush.objects.all()
    serializer_class = BrushSerializer




# Serializers define the API representation.
class PatternSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pattern
        fields = ('name', 'description')

# ViewSets define the view behavior.
class PatternViewSet(viewsets.ModelViewSet):
    queryset = Pattern.objects.all()
    serializer_class = PatternSerializer
