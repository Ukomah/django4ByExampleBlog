from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import EmailPostForm
from django.core.mail import send_mail

# Create your views here.

def postList(request):
    postList = Post.published.all()
    paginator = Paginator(postList, 2)
    page_number = request.GET.get('page', 1)
    
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page
        posts = paginator.page(paginator.num_pages)
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
    
    
    
def sharePost(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False # Add a flag to track whether the email has been sent
    
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} ({cd['email']}) recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'henryukomah@gmail.com', [cd['to']])
            sent = True  # Set the flag to True when the email is sent
    else:
        form = EmailPostForm()
    return render(request,
                  'blog/post/sharePost.html',
                  {'post': post,
                   'form': form,
                   'sent': sent})