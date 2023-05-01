from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
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
    slug = models.SlugField(max_length=255)
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