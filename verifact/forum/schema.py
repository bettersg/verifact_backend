from graphene import relay, ObjectType, String, Field, ID, Boolean
from graphene.relay import Node, ClientIDMutation
from graphql_relay.node.node import from_global_id
from graphene_django import DjangoObjectType
import base64
from graphql import GraphQLError
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from graphql_jwt.decorators import login_required
from .. import error_strings
from .models import Question, Answer, Vote
from verifact.graph.scalars import Url

class QuestionNode(DjangoObjectType):
    class Meta:
        model = Question
        interfaces = (relay.Node,)


class AnswerNode(DjangoObjectType):
    class Meta:
        model = Answer
        interfaces = (relay.Node,)
        convert_choices_to_enum = False

class VoteNode(DjangoObjectType):
    class Meta:
        model = Vote
        interfaces = (relay.Node,)

class QuestionConnection(relay.Connection):
    class Meta:
        node = QuestionNode

class AnswerConnection(relay.Connection):
    class Meta:
        node = AnswerNode

class VoteConnection(relay.Connection):
    class Meta:
        node = VoteNode

class Query(ObjectType):
    questions = relay.ConnectionField(QuestionConnection)
    answers = relay.ConnectionField(AnswerConnection)
    votes = relay.ConnectionField(VoteConnection)

    def resolve_questions(root, info):
        return Question.objects.all()


class QuestionCreate(ClientIDMutation):
    question = Field(QuestionNode)

    class Input:
        text = String(required=True)
        citation_url = Url(required=True)
        citation_title = String()
        citation_image_url = Url()

    @login_required
    def mutate_and_get_payload(
        self, info, text, citation_url, citation_title="", citation_image_url=""
    ):
        viewer = info.context.user
        question = Question.objects.create(
            text=text,
            citation_url=citation_url,
            citation_title=citation_title,
            citation_image_url=citation_image_url,
            user=viewer
        )
        return QuestionCreate(question=question)


class AnswerCreate(ClientIDMutation):
    answer = Field(AnswerNode)

    class Input:
        answer = String(required=True)
        text = String()
        citation_url = Url()
        citation_title = String()
        question_id = ID(required=True)

    @login_required
    def mutate_and_get_payload(
        self,
        info,
        answer,
        text,
        question_id,
        citation_url="",
        citation_title="",
    ):
        viewer = info.context.user
        try:
            answer = Answer.objects.create(
                answer=answer,
                text=text,
                citation_url=citation_url,
                citation_title=citation_title,

                question=Node.get_node_from_global_id(
                    info, question_id, only_type=QuestionNode
                ),
                user=viewer
            )
        except IntegrityError as ie:
            if str(ie.__cause__).startswith(
                'new row for relation "forum_answer" violates check constraint "forum_answer_answer_valid"'
            ):
                raise GraphQLError(error_strings.ANSWER_CHOICES_INVALID)
            else:
                raise
        except AssertionError as ae:
            if str(ae).startswith("Must receive a QuestionNode id."):
                raise GraphQLError(error_strings.ANSWER_QUESTION_ID_INVALID)
            else:
                raise

        return AnswerCreate(answer=answer)

class VoteCreateUpdateDelete(ClientIDMutation):
    vote = Field(VoteNode)

    class Input:
        credible = Boolean() # if null, remove vote!
        answer_id = ID(required=True)

    #@login_required
    def mutate_and_get_payload(
        self,
        info,
        answer_id,
        **kwargs
    ):
        credible = kwargs.get('credible',None)
        vote=None
        viewer = info.context.user
        answer_pk = from_global_id(answer_id)[1]
        vote_already_exists = True
        try:
            vote = Vote.objects.get(user=viewer,answer=answer_pk)
        except ObjectDoesNotExist as dne:
            vote_already_exists = False

        if vote_already_exists:
            if credible is None: # if vote null, delete
                vote.delete()
                return VoteCreateUpdateDelete(vote = None)
            else:
                vote.credible = credible
                vote.save()
        else:
            if credible is not None:
                vote = Vote.objects.create(
                    user=viewer,
                    answer=Node.get_node_from_global_id(
                        info, answer_id, only_type=AnswerNode
                    ),
                    credible=credible
                )


        return VoteCreateUpdateDelete(vote=vote)


class Mutation(ObjectType):
    question_create = QuestionCreate.Field()
    answer_create = AnswerCreate.Field()
    vote_create_update_delete = VoteCreateUpdateDelete.Field()
