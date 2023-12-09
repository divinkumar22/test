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
        resp = {"status": 0, "message": "Something went wrong"}
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
            resp['status'] = 1
            resp['message'] = "User Post Saved"
        else:
            resp['status'] = 0
            resp['message'] = serializer_data.errors

        return Response(resp)
class UserPostAnalysis(APIView):

    def get(self,request,post_id):
        resp = {"response":{},"status":0}
        user_id = request.user.id 
        user_post = Post.objects.filter(user_id = user_id,id =post_id).first()
        if user_post:
            text = user_post.text
            list_word = text.split(' ')
            total_word = len(list_word)
            words_total_len = 0
            for words  in list_word:
                len_word  =  len(words)
                words_total_len = words_total_len+len_word
            resp['total_words'] = total_word
            resp['avg_words'] = words_total_len/total_word
            resp['status'] = 1
        return Response(resp)

                
                

            

            

