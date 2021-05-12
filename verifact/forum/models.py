from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

class Citation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="citations")
    url = models.CharField(max_length=2048)
    title = models.CharField(max_length=2048)
    image_url = models.CharField(max_length=2048)

    limit_content = models.Q(app_label="forum", model="answer") | models.Q(app_label="forum", model="question")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=limit_content)
    content_pk = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'content_pk')

    def __str__(self):
        return f"{self.url}"


class Question(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=2048)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="questions")
    citations = GenericRelation(Citation, related_query_name="question",object_id_field='content_pk', content_type_field='content_type')
    def __str__(self):
        return self.text


class Answer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    answer = models.CharField(
        choices=[
            ("True", "True"),
            ("False", "False"),
            ("Neither", "Neither"),
        ],
        max_length=8,
    )
    text = models.CharField(max_length=2048)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="answers")
    citations = GenericRelation(Citation, related_query_name="answer",object_id_field='content_pk', content_type_field='content_type')

    def __str__(self):
        return "[%s] %s" % (self.get_answer_display(), self.text)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_answer_valid",
                check=models.Q(answer__in=["True", "False", "Neither"])
            )
        ]

class Vote(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="votes")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE,related_name="votes")
    credible = models.BooleanField()

    def __str__(self):
        return f"{self.credible}:{self.answer.text}"
