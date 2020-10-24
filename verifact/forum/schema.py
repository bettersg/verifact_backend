from graphene import relay, ObjectType, Mutation
from graphene import DateTime, String, Int, Field
from graphene_django import DjangoObjectType
import base64
from graphql import GraphQLError
from django.db import IntegrityError
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

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



class QuestionCreate(Mutation):
    class Arguments:
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
        citation_title="",
        citation_image_url="",
    ):
        val = URLValidator()
        try:
            val(citation_url)
        except ValidationError:
            raise GraphQLError('citationUrl has invalid format!')
        question = Question.objects.create(
            text=text,
            citation_url=citation_url,
            citation_title=citation_title,
            citation_image_url=citation_image_url
            )

        question.save()
        return QuestionCreate(question=question)


class AnswerCreate(Mutation):
    class Arguments:
        answer = String()
        text = String()
        citation_url = String()
        citation_title = String()
        question_id = String()

    answer = Field(AnswerNode)

    def mutate(
        self,
        info,
        answer,
        text,
        question_id,
        citation_url="",
        citation_title="",
    ):
        val = URLValidator()
        try:
            val(citation_url)
        except ValidationError:
            raise GraphQLError('citationUrl has invalid format!')

        try:
            answer = Answer.objects.create(
                answer=answer,
                text=text,
                citation_url=citation_url,
                citation_title=citation_title,
                credible_count=0,
                not_credible_count=0,
                question=Question.objects.get(
                    pk=int(base64.b64decode(question_id.encode()).decode().split(':')[1])
                ),
            )
            answer.save()
        except IntegrityError as e:
            if str(e.__cause__).startswith('new row for relation "forum_answer" violates check constraint "forum_answer_answer_valid"'): # this works but looks kinda bandaidy
                raise GraphQLError('answer must be True, False, or Neither')
            else:
                raise

        return AnswerCreate(answer=answer)


class Mutation(ObjectType):
    question_create = QuestionCreate.Field()
    answer_create = AnswerCreate.Field()
