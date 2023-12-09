from rest_framework import status
import hashlib
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializer import UserPostSerializers

class UserPostView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user_id = request.user.id
        data['user_id'] = request.user.id

        # Create a hash key from the text
        text = data['text']
        hash_key = hashlib.sha256(text.encode()).hexdigest()
        data['unique_key'] = hash_key

        # Use the serializer with the custom validator
        serializer_data = UserPostSerializers(data=data, context={'request': request})

        if serializer_data.is_valid():
            serializer_data.save()
            return Response({"status": 1, "message": "User Post Saved"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": 0, "message": "Failed to save user post", "errors": serializer_data.errors},
                            status=status.HTTP_400_BAD_REQUEST)


class UserPostAnalysis(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        user_id = request.user.id
        user_post = Post.objects.filter(user_id=user_id, id=post_id).first()

        if user_post:
            text = user_post.text
            list_words = text.split(' ')
            total_words = len(list_words)

            if total_words > 0:
                words_total_len = sum(len(word) for word in list_words)

                return Response({
                    "status": 1,
                    "message": "User Post Analysis Successful",
                    "total_words": total_words,
                    "avg_words": words_total_len / total_words
                })
            else:
                return Response({"status": 0, "message": "No words found in the post for analysis"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"status": 0, "message": "User Post not found"},
                            status=status.HTTP_404_NOT_FOUND)
