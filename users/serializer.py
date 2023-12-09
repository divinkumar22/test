from rest_framework.serializers import ModelSerializer
from .models import Post


class UserPostSerializers(ModelSerializer):
    
    class Meta:
        model = Post
        fields = ['text','user_id']