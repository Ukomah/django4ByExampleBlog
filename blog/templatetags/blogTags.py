from django import template
from ..models import Post
from django.db.models import Count

register = template.Library()

@register.simple_tag
def totalPosts():
    return Post.published.count()

@register.inclusion_tag('blog/post/latestPosts.html')
def showLatestPosts(count=5):
    latestPosts = Post.published.order_by('-publish')[:count]
    return {'latestPosts':latestPosts}

@register.simple_tag
def getMostCommentedPosts(count=5):
    return Post.published.annotate(comment_count=Count('comments')).order_by('-comment_count')[:count]