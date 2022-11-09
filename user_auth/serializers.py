from rest_framework import serializers
from .models import * 



class AuthUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","username" , "email" ,"is_active" , "is_verified" , "created_at" ,"is_admin")
        extra_kwargs = {'password': {'write_only': True}, 'is_active':{'read_only':True} , 'is_admin':{'read_only':True} , 'is_verified':{'read_only':True} }
        