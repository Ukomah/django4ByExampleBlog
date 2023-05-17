
import factory
from django.contrib.auth.models import User
from blog.models import Post, Comment

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Sequence(lambda n: f"user{n}@test.com")

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Sequence(lambda n: f"Post Title {n}")
    slug = factory.Sequence(lambda n: f"post-title-{n}")
    author = factory.SubFactory(UserFactory)
    body = factory.Faker('paragraph')
    

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    body = factory.Faker('sentence')
    post = factory.SubFactory(PostFactory)
