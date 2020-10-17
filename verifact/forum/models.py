from django.db import models
from django.utils.translation import gettext_lazy as _


class Question(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=2048)
    citation_url = models.CharField(max_length=512)
    citation_title = models.CharField(max_length=512)
    citation_image_url = models.CharField(max_length=512)

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
    citation_url = models.CharField(max_length=2048)
    citation_title = models.CharField(max_length=2048)
    credible_count = models.IntegerField()
    not_credible_count = models.IntegerField()
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )

    def __str__(self):
        return "[%s] %s" % (self.get_answer_display(), self.text)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_answer_valid",
                check=models.Q(answer__in=["True", "False", "Neither"])
            )
        ]
