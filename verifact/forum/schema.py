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
        convert_choices_to_enum = False


class QuestionConnection(relay.Connection):
    class Meta:
        node = QuestionNode


class AnswerConnection(relay.Connection):
    class Meta:
        node = AnswerNode


class Query(ObjectType):
    question = relay.Node.Field(QuestionNode)
    questions = relay.ConnectionField(QuestionConnection)

    answer = relay.Node.Field(AnswerNode)
    answers = relay.ConnectionField(AnswerConnection)

    def resolve_questions(root, info):
        return Question.objects.all()

    def resolve_answers(root, info):
        return Answer.objects.all()
