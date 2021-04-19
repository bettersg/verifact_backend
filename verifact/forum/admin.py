from django.contrib import admin
from .models import Question, Answer, Vote


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass

@admin.register(Vote)
class AnswerAdmin(admin.ModelAdmin):
    pass
