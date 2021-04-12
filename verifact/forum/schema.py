from graphene import relay, ObjectType, String, Field, ID, Boolean, List
from graphene.relay import Node, ClientIDMutation
from graphql_relay.node.node import from_global_id
from graphene_django import DjangoObjectType
import base64
from graphql import GraphQLError
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from graphql_jwt.decorators import login_required
from .. import error_strings
from .models import Question, Answer, Vote, Citation
from verifact.graph.scalars import Url
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse


class CitationNode(DjangoObjectType):
    class Meta:
        model = Citation
        interfaces = (relay.Node,)

class QuestionNode(DjangoObjectType):
    class Meta:
        model = Question
        interfaces = (relay.Node,)

    citations = List(CitationNode)
    def resolve_citations(self, args):
        return self.citations.all()

class AnswerNode(DjangoObjectType):
    class Meta:
        model = Answer
        interfaces = (relay.Node,)
        convert_choices_to_enum = False

    citations = List(CitationNode)
    def resolve_citations(self, args):
        return self.citations.all()

class VoteNode(DjangoObjectType):
    class Meta:
        model = Vote
        interfaces = (relay.Node,)

class CitationConnection(relay.Connection):
    class Meta:
        node = CitationNode

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

    def resolve_questions(root, info):
        return Question.objects.all()


class QuestionCreate(ClientIDMutation):
    question = Field(QuestionNode)

    class Input:
        text = String(required=True)

    @login_required
    def mutate_and_get_payload(
        self, info, text,
    ):
        viewer = info.context.user
        question = Question.objects.create(
            text=text,
            user=viewer
        )
        return QuestionCreate(question=question)


class AnswerCreate(ClientIDMutation):
    answer = Field(AnswerNode)

    class Input:
        answer = String(required=True)
        text = String()
        question_id = ID(required=True)

    @login_required
    def mutate_and_get_payload(
        self,
        info,
        answer,
        text,
        question_id,
    ):
        viewer = info.context.user
        try:
            answer = Answer.objects.create(
                answer=answer,
                text=text,
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

    @login_required
    def mutate_and_get_payload(
        self,
        info,
        answer_id,
        **kwargs
    ):
        credible = kwargs.get('credible',None)
        viewer = info.context.user
        answer_pk = from_global_id(answer_id)[1]
        vote=None
        try:
            vote = Vote.objects.get(user=viewer,answer=answer_pk)
            if credible is None:
                vote.delete()
            else:
                vote.credible = credible
                vote.save()
        except ObjectDoesNotExist:
            if credible is not None:
                vote = Vote.objects.create(
                    user=viewer,
                    answer=Answer.objects.get(id=answer_pk),
                    credible=credible
                )

        return VoteCreateUpdateDelete(vote=vote)

class CitationCreate(ClientIDMutation):
    citation = Field(CitationNode)

    class Input:
        citation_url = Url(required=True)
        parent_id = ID(required=True)

    @login_required
    def mutate_and_get_payload(
        self,
        info,
        citation_url,
        parent_id
    ):
        viewer = info.context.user
        parent_type = from_global_id(parent_id)[0]
        parent_pk = from_global_id(parent_id)[1]

        parent_class = None
        if parent_type == "QuestionNode":
            parent_class = Question
        elif parent_type == "AnswerNode":
            parent_class = Answer
        else:
            raise GraphQLError(error_strings.CITATION_PARENT_MUST_BE_QUESTION_ANSWER)

        parent_object = parent_class.objects.get(id=parent_pk)

        try:
            url_content = requests.get(citation_url,headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'}).content
            url_soup = BeautifulSoup(url_content,features="html.parser")
            citation_image_url = url_soup.find("meta",{"property":"og:image","content":True})['content']
            citation_title = url_soup.find("meta",{"property":"og:title","content":True})['content']
        except (TypeError, requests.exceptions.RequestException) as e:
            citation_image_url = "https://d1nhio0ox7pgb.cloudfront.net/_img/o_collection_png/green_dark_grey/256x256/plain/symbol_questionmark.png"
            citation_title = f"Site: {urlparse(citation_url).netloc}"


        citation = Citation.objects.create(
            user=viewer,
            citation_url=citation_url,
            citation_image_url=citation_image_url,
            citation_title=citation_title,
            parent_object=parent_object,
        )


        return CitationCreate(citation=citation)

class Mutation(ObjectType):
    question_create = QuestionCreate.Field()
    answer_create = AnswerCreate.Field()
    vote_create_update_delete = VoteCreateUpdateDelete.Field()
    citation_create = CitationCreate.Field()
