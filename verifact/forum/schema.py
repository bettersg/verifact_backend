from graphene import relay, ObjectType, String, Field, ID
from graphene.relay import Node, ClientIDMutation
from graphene_django import DjangoObjectType
import base64
from graphql import GraphQLError
from django.db import IntegrityError
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from .. import error_strings
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
    questions = relay.ConnectionField(QuestionConnection)
    answers = relay.ConnectionField(AnswerConnection)

    def resolve_questions(root, info):
        return Question.objects.all()

    def resolve_answers(root, info):
        return Answer.objects.all()


class QuestionCreate(ClientIDMutation):
    question = Field(QuestionNode)

    class Input:
        text = String()
        citation_url = String()
        citation_title = String()
        citation_image_url = String()

    def mutate_and_get_payload(
        self, info, text, citation_url, citation_title="", citation_image_url=""
    ):
        try:
            URLValidator(citation_url)
        except ValidationError:
            raise GraphQLError(error_strings.URL_FORMAT_INVALID)
        question = Question.objects.create(
            text=text,
            citation_url=citation_url,
            citation_title=citation_title,
            citation_image_url=citation_image_url,
        )

        question.save()
        return QuestionCreate(question=question)


class AnswerCreate(ClientIDMutation):
    answer = Field(AnswerNode)

    class Input:
        answer = String()
        text = String()
        citation_url = String()
        citation_title = String()
        question_id = ID()

    def mutate_and_get_payload(
        self,
        info,
        answer,
        text,
        question_id,
        citation_url="",
        citation_title="",
    ):
        try:
            URLValidator(citation_url)
        except ValidationError:
            raise GraphQLError(error_strings.URL_FORMAT_INVALID)

        try:
            answer = Answer.objects.create(
                answer=answer,
                text=text,
                citation_url=citation_url,
                citation_title=citation_title,
                credible_count=0,
                not_credible_count=0,
                question=Node.get_node_from_global_id(
                    info, question_id, only_type=QuestionNode
                ),
            )
            answer.save()
        except IntegrityError as ie:
            if str(ie.__cause__).startswith(
                'new row for relation "forum_answer" violates check constraint "forum_answer_answer_valid"'
            ):
                raise GraphQLError(error_strings.ANSWER_CHOICES_INVALID)
            else:
                raise
        except AssertionError as ae:
            if str(ae).startswith("Must receive a QuestionNode id."):
                raise GraphQLError(error_strings.QUESTION_ID_INVALID)
            else:
                raise

        return AnswerCreate(answer=answer)


class Mutation(ObjectType):
    question_create = QuestionCreate.Field()
    answer_create = AnswerCreate.Field()
