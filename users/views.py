from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializer import UserPostSerializers
from .models import Post


class UserPostView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        resp = {"status":0,"message":"somthing Wrong"}
        data = request.data
        user_id = request.user.id
        data['user_id'] = request.user.id
        serlizer_data = UserPostSerializers(data=data)
        if serlizer_data.is_valid():
            serlizer_data.save()
            resp['status']=1
            resp['message']= "User Post Saved"
        else:
            resp['status'] = 0
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

                
                

            

            

