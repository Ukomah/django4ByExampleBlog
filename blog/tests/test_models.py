
import os
import sys
sys.path.append(r'\Users\User\Desktop\PY4E\django4ByPracticeBlog\blogsite')  # Replace this with the actual path

os.environ['DJANGO_SETTINGS_MODULE'] = 'blogsite.settings'
import django
django.setup()

import pytest
from django.urls import reverse
from django.core.exceptions import ValidationError
from .factories import PostFactory, CommentFactory
from blog.models import Post, Comment 
from django.db import DataError

pytestmark = pytest.mark.django_db

class TestPostModel:
    def test_str_return(self):
        post = PostFactory()
        assert str(post) == post.title

    def test_field_validation(self):
        with pytest.raises(DataError):
            post = PostFactory(title='a'*256)
            post.full_clean()

    def test_get_absolute_url(self):
        post = PostFactory()
        expected_url = reverse('blog:postDetails', args=[post.publish.year, post.publish.month, post.publish.day, post.slug])
        assert post.get_absolute_url() == expected_url  # Replace with your actual URL pattern


    def test_related_name(self):
        post = PostFactory()
        comment = CommentFactory(post=post)
        assert comment in post.comments.all()

    def test_cascade_delete(self):
        post = PostFactory()
        comment = CommentFactory(post=post)
        post.delete()
        assert not Comment.objects.filter(id=comment.id).exists()