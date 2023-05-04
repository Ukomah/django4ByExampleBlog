from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse
# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PD', 'Published'
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    image = image = models.FileField(blank=True, null=True, upload_to='images/')
    body = RichTextField(blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                                     choices=Status.choices,
                                     default=Status.DRAFT)
    objects = models.Manager()          # the default manager
    published = PublishedManager()      # my defined manager
    
    
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields =['-publish']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:postDetails', args=[self.publish.year, 
                                              self.publish.month,
                                              self.publish.day,
                                              self.slug])

    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
        
    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields =['created']),
        ]
            
    def __str__(self):
        return f'Coment by {self.name} on {self.post}'
            