from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlogModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    youtube_title = models.CharField(max_length=200)
    youtube_link = models.URLField(max_length=200)
    blog_article = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.youtube_title 