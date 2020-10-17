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
    class AnswerTypes(models.IntegerChoices):
        TRUE = 1, _("True")
        FALSE = 2, _("False")
        NEITHER = 3, _("Neither")

    created_at = models.DateTimeField(auto_now_add=True)
    answer = models.IntegerField(choices=AnswerTypes.choices)
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
