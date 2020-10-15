from django.db import models


class Question(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=2048)
    citation_url = models.CharField(max_length=512)
    citation_title = models.CharField(max_length=512)
    citation_image_url = models.CharField(max_length=512)

    def __str__(self):
        return self.text
