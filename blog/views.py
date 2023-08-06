from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from taggit.models import Tag



# Create your views here.
def about(request):
    return render(request, 'blog/about.html')

def portfolio(request):
    return render(request, 'blog/portfolio.html')

def postList(request, tag_slug=None):
    postList = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        postList = postList.filter(tags__in=[tag])       
        
    paginator = Paginator(postList, 4)
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
                  {'posts': posts,
                  'tag':tag})
    
    
def postDetails(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = Comment.objects.filter(post=post, active=True)
    form = CommentForm()
    
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')
    
    return render(request,
                    'blog/post/postDetails.html',
                    {'post': post,
                    'comments': comments,
                    'form': form,
                    'similar_posts': similar_posts})
        

    
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
    
    
    
@require_POST
def postComment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    form = CommentForm(data=request.POST)
    comment = None
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect(post.get_absolute_url())  # Redirect to the post
    else:
        return render(request,
                      'blog/post/postComment.html',
                      {'post': post,
                       'comment': comment,
                       'form': form})
    
    
def postSearch(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            
            # Update this part to search both title and body fields
            title_similarity = TrigramSimilarity('title', query)
            body_similarity = TrigramSimilarity('body', query)
            
            results = Post.published.annotate(
                similarity = title_similarity + body_similarity,
            ).filter(
                Q(similarity__gt=0.3) | Q(title__icontains=query) | Q(body__icontains=query)
            ).order_by('-similarity')

    return render(request,
                  'blog/post/postSearch.html',
                  {'form': form,
                  'query': query,
                  'results': results
                  })
        
        

def tagView(request):
    all_tags = Tag.objects.all()  # This fetches all tags used across all posts.
    return render(request, 'post.html', {'all_tags': all_tags})