from rest_framework.serializers import ModelSerializer 
from .models import *

class PolicySerializer(ModelSerializer):
    class Meta:
        model = Policy 
        fields = ['category', 'name', 'fullText', 'link', 'author', 'id', 'date', 'slug']
        lookup_field = 'slug'
    
class ElementSerializer(ModelSerializer):
    class Meta:
        model = Element
        fields = "__all__"

class ElementFlagSerializer(ModelSerializer):
    element = ElementSerializer(read_only=True)
    class Meta:
        model = ElementFlag
        fields = "__all__"