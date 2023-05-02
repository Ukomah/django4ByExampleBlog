from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator

# Create your views here.

def postList(request):
    postList = Post.published.all()
    paginator = Paginator(postList, 2)
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)
    
    return render(request,
                  'blog/post/postList.html',
                  {'posts': posts})
    
    
def postDetails(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/postDetails.html',
                  {'post': post})