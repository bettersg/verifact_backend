from graphene import relay, ObjectType
from graphene_django import DjangoObjectType

from .models import Question


class QuestionNode(DjangoObjectType):
    class Meta:
        model = Question
        interfaces = (relay.Node,)


class QuestionConnection(relay.Connection):
    class Meta:
        node = QuestionNode


class Query(ObjectType):
    question = relay.Node.Field(QuestionNode)
    questions = relay.ConnectionField(QuestionConnection)

    def resolve_questions(root, info):
        return Question.objects.all()
