from django.db import models
from django.utils.translation import gettext_lazy as _


class Question(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=2048)
    citation_url = models.CharField(max_length=512)
    citation_title = models.CharField(max_length=512)
    citation_image_url = models.CharField(max_length=512)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="questions")

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
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="answers")

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
    credible = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.credible}:{self.answer.text}"
