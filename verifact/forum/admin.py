from django.contrib import admin
from .models import Question, Answer


@admin.register(Question, Answer)
class QuestionAdmin(admin.ModelAdmin):
    pass
