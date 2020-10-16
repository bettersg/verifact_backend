from graphene import DateTime, String, Field
from graphene import relay, ObjectType, Mutation
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


# MUTATIONS


class CreateQuestion(Mutation):
    class Arguments:
        created_at = DateTime()
        text = String()
        citation_url = String()
        citation_title = String()
        citation_image_url = String()

    question = Field(QuestionNode)

    def mutate(
        self,
        info,
        text,
        citation_url,
        citation_title=None,
        citation_image_url=None,
        created_at=None,
    ):
        question = Question.objects.create(
            text=text,
            citation_url=citation_url,
            citation_title=citation_title if citation_title is not None else "Untitled",  # TODO: fetch with OpenGraph if not supplied
            citation_image_url=citation_image_url if citation_image_url is not None else "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Noun_Project_question_mark_icon_1101884_cc.svg/1024px-Noun_Project_question_mark_icon_1101884_cc.svg.png",  # TODO: fetch with OpenGraph if not supplied
            created_at=created_at,
        )

        question.save()
        return CreateQuestion(question=question)


class Mutation(ObjectType):
    create_question = CreateQuestion.Field()
