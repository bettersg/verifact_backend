from django.contrib import admin
from .models import Question, Answer, Vote, Citation


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    pass

@admin.register(Citation)
class CitationAdmin(admin.ModelAdmin):
    pass
