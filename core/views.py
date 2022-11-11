from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from .models import *
from . serializers import *
from django.contrib.auth.hashers import make_password
import jwt
from rest_framework import exceptions
from django.conf import settings
from rest_framework import permissions
import random
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.utils import timezone



class PostView(APIView):
    def get(self, request):
        try:
            user_id = request.user.id
            queryset = Post.objects.filter(user__id = user_id).order_by("-id")
            serializers = PostSerializers(queryset , many = True)
            return JsonResponse({"status":status.HTTP_200_OK , "data":serializers.data})
        except Exception as e:
            return JsonResponse({"status":status.HTTP_500_INTERNAL_SERVER_ERROR , "msg":e.args[0]})

    def post(self,request):
        try:
            data = request.data
            serializers = PostSerializers(data=data)
            serializers.is_valid(raise_exception=True)
            serializers.save(user = request.user)
            return JsonResponse({"status":status.HTTP_201_CREATED , "data":serializers.data})
        except Exception as e :
            return JsonResponse({"status":status.HTTP_500_INTERNAL_SERVER_ERROR , "msg":e.args[0]})


    def put(self, request,pk, format=None):
        try:
            user_id = request.user.id
            query = Post.objects.filter(id=pk).last()
            if user_id == query.user.id:
                serializer = PostSerializers(
                    instance=query, data=request.data, partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_200_OK)

            else:
                return JsonResponse(
                    {
                        "status": status.HTTP_401_UNAUTHORIZED,
                        "msg": "You do not have permision to update the post",
                    }
                )
        except Exception as e:
            return JsonResponse(
                {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "msg": e.args[0]}
            )

class FriendsView(APIView):
    def get(self , request):
        try:
            user_id = request.user.id
            query_set = Connections.objects.filter(user__id = user_id).order_by("-id")
        except:
            pass