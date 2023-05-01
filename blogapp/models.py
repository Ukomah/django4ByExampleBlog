from django.db import models
from django.utils import timezone
# Create your models here.
class Post(models.Model):
    
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PD', 'Published'
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.models.CharField(max_length=2,
                                     choices=Status.choices,
                                     default=Status.DRAFT)
    
    
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields =['-publshed']),
        ]
    
    def __str__(self):
        return self.title