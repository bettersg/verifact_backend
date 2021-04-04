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
    citation_url = factory.Faker("url")
    citation_title = factory.Faker("sentence")
    citation_image_url = factory.Faker("image_url")
    user = None


class Answer(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Answer

    created_at = factory.LazyFunction(timezone.now)
    answer = factory.LazyAttribute(lambda a: random.choice(["True", "False", "Neither"]))
    text = factory.Faker("paragraph")
    citation_url = factory.Faker("url")
    citation_title = factory.Faker("sentence")
    credible_count = factory.LazyAttribute(lambda a: random.randrange(10))
    not_credible_count = factory.LazyAttribute(lambda a: random.randrange(10))
    question = None
    user = None
