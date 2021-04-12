import factory
import random
from django.utils import timezone
from django.contrib.auth.models import User

from verifact.forum import models


class User(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "%s%s" % (factory.Faker("user_name"), n))
    email = factory.LazyAttribute(lambda o: "%s@example.com" % o.username)
    password = "password"


class Question(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Question

    created_at = factory.LazyFunction(timezone.now)
    text = factory.Faker("paragraph")
    user = None


class Answer(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Answer

    created_at = factory.LazyFunction(timezone.now)
    answer = factory.LazyAttribute(
        lambda a: random.choice(["True", "False", "Neither"])
    )
    text = factory.Faker("paragraph")
    question = None
    user = None


class Vote(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Vote

    created_at = factory.LazyFunction(timezone.now)
    credible = factory.Faker("pybool")
    user = None
    answer = None


class Citation(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Citation

    created_at = factory.LazyFunction(timezone.now)
    user = None
    parent_object = None
    citation_image_url = None
    citation_title = None
    citation_url = factory.Faker("url")
