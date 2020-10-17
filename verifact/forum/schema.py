from graphene import relay, ObjectType
from graphene_django import DjangoObjectType

from .models import Question, Answer


class QuestionNode(DjangoObjectType):
    class Meta:
        model = Question
        interfaces = (relay.Node,)


class AnswerNode(DjangoObjectType):
    class Meta:
        model = Answer
        interfaces = (relay.Node,)


class QuestionConnection(relay.Connection):
    class Meta:
        node = QuestionNode


class Query(ObjectType):
    question = relay.Node.Field(QuestionNode)
    questions = relay.ConnectionField(QuestionConnection)

    answer = relay.Node.Field(AnswerNode)
    answers = relay.ConnectionField(AnswerNode)

    def resolve_questions(root, info):
        return Question.objects.all()

    def resolve_answers(root, info):
        return Answer.objects.all()
