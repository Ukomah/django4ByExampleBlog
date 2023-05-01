from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.

def postList(request):
    posts = Post.published.all()
    return render(request,
                  'blog/postList.html',
                  {'posts': posts})
    
    
def postDetails(request):
    post = get_object_or_404(Post,
                             id=id,
                             status=Post.Status.PUBLISHED)
    return render(request,
                  'blog/postDetails.html',
                  {'post': post})