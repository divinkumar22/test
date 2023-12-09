from rest_framework.serializers import ModelSerializer
from .models import Post


from rest_framework import serializers
from .models import Post

class UserPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['text', 'user_id','unique_key']

    def validate_unique_key(self, value):
        """
        Custom validator to check if the unique_key is unique.
        """
        user_id = self.context['request'].user.id
        existing_post = Post.objects.filter(user_id=user_id, unique_key=value).first()
        if existing_post:
            raise serializers.ValidationError("Post with this text already exists")

        return value