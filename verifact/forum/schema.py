from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Question, Answer


class QuestionNode(DjangoObjectType):
    class Meta:
        model = Question
        interfaces = (relay.Node,)


class AnswerNode(DjangoObjectType):
    class Meta:
        model = Answer
        filter_fields = {"question_id": ["exact"]}
        interfaces = (relay.Node,)


class QuestionConnection(relay.Connection):
    class Meta:
        node = QuestionNode


class Query(ObjectType):
    question = relay.Node.Field(QuestionNode)
    questions = relay.ConnectionField(QuestionConnection)

    answer = relay.Node.Field(AnswerNode)
    answers = DjangoFilterConnectionField(AnswerNode)

    def resolve_questions(root, info):
        return Question.objects.all()

    def resolve_answers(root, info):
        return Answer.objects.all()
