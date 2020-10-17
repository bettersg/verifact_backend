from django.contrib import admin
from .models import Question, Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(Answers)
class AnswerAdmin(admin.ModelAdmin):
    pass
