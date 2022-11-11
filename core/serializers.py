from rest_framework import serializers
from .models import * 



class PostSerializers(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(method_name="get_like")
    comments= serializers.SerializerMethodField(method_name="get_comments")
    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "content",
            "img",
            "likes",
            "comments"
        )

    def get_like(self,instance):
        try:
            post_id = instance.id
            total_like = Like.objects.filter(post__id = post_id).count()
        except:
            total_like = 0
        return total_like 
    
            
           
    def get_like(self,instance):
        try:
            post_id = instance.id
            queryset = Comment.objects.filter(post__id = post_id).order_by("-id")
            serializers = CommentSerializer(queryset , many = True)
            comments = serializers.data
        except:
            comments = {}
        return comments 
    
            
           
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment 
        fields = "__all__"
