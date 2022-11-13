from django.db import models
from user_auth . models import User 

class Connections(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    follows = models.ForeignKey( User,
        on_delete=models.CASCADE,
        related_name="followed_by",
        blank=True
    )
    is_connected = models.BooleanField(default = False)


class Post(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE , related_name = "post")
    content = models.TextField(default = "",null = True , blank =True)
    img = models.ImageField(null =True, blank=True)
    connections = models.ForeignKey(Connections , on_delete=models.CASCADE, null = True,blank = True , related_name = "friends")

    def __str__(self):
        return str(self)

class Like(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    is_liked = models.BooleanField(default = False)

class Comment(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    content = models.TextField(default = "" , null=True,blank=True)




    