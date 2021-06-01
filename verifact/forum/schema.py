from graphene import relay, ObjectType, String, Field, ID, Boolean, List, NonNull, JSONString
from graphene.relay import Node, Connection, ConnectionField, ClientIDMutation
from graphql_relay.node.node import from_global_id
from graphene_django import DjangoObjectType
from django_filters import FilterSet, OrderingFilter
from graphene_django.filter import DjangoFilterConnectionField
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

class CitationConnection(Connection):
    class Meta:
        node = CitationNode

class QuestionFilter(FilterSet):
    order_by = OrderingFilter(
        fields=(
            ("created_at",)
        )
    )

    class Meta:
        model = Question
        fields = []


class VoteNode(DjangoObjectType):
    class Meta:
        model = Vote
        interfaces = (relay.Node,)


class QuestionNode(DjangoObjectType):
    class Meta:
        model = Question
        interfaces = (relay.Node,)
        filterset_class = QuestionFilter

    citations = ConnectionField(CitationConnection)

    def resolve_citations(self, args):
        return self.citations.all()


class AnswerNode(DjangoObjectType):
    class Meta:
        model = Answer
        interfaces = (relay.Node,)
        convert_choices_to_enum = False

    citations = ConnectionField(CitationConnection)
    viewer_vote = Field(VoteNode)

    def resolve_citations(self, args):
        return self.citations.all()

    def resolve_viewer_vote(self, args):
        try:
            return Vote.objects.get(answer=self, user=args.context.user)
        except Vote.DoesNotExist:
            return None


class Query(ObjectType):
    questions = DjangoFilterConnectionField(QuestionNode,)


def citation_create_mutation(url, content, user):
    try:
        url_content = requests.get(
            url,
            headers={
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0"
            },
        ).content
        url_soup = BeautifulSoup(url_content, features="html.parser")
        image_url = url_soup.find("meta", {"property": "og:image", "content": True})[
            "content"
        ]
        title = url_soup.find("meta", {"property": "og:title", "content": True})[
            "content"
        ]
    except (TypeError, requests.exceptions.RequestException) as e:
        image_url = "https://d1nhio0ox7pgb.cloudfront.net/_img/o_collection_png/green_dark_grey/256x256/plain/symbol_questionmark.png"
        title = f"Site: {urlparse(url).netloc}"

    citation = Citation.objects.create(
        user=user,
        url=url,
        image_url=image_url,
        title=title,
        content_object=content,
    )


class QuestionCreate(ClientIDMutation):
    question = Field(QuestionNode)

    class Input:
        text = String(required=True)
        citation_urls = List(NonNull(Url))

    @login_required
    def mutate_and_get_payload(self, info, text, citation_urls):
        viewer = info.context.user

        if len(citation_urls) == 0:
            raise GraphQLError(error_strings.ANSWER_QUESTION_MINIMUM_ONE_CITATION)

        question = Question.objects.create(text=text, user=viewer)

        for url in citation_urls:
            citation_create_mutation(url, question, viewer)

        return QuestionCreate(question=question)


class AnswerCreate(ClientIDMutation):
    answer = Field(AnswerNode)

    class Input:
        answer = String(required=True)
        text = String(required=True)
        question_id = ID(required=True)
        citation_urls = List(NonNull(Url))

    @login_required
    def mutate_and_get_payload(self, info, answer, text, question_id, citation_urls):
        viewer = info.context.user
        if len(citation_urls) == 0:
            raise GraphQLError(error_strings.ANSWER_QUESTION_MINIMUM_ONE_CITATION)

        try:
            answer = Answer.objects.create(
                answer=answer,
                text=text,
                question=Node.get_node_from_global_id(
                    info, question_id, only_type=QuestionNode
                ),
                user=viewer,
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

        for url in citation_urls:
            citation_create_mutation(url, answer, viewer)

        return AnswerCreate(answer=answer)


class VoteCreateUpdateDelete(ClientIDMutation):
    vote = Field(VoteNode)

    class Input:
        credible = Boolean() # if null, remove vote!
        answer_id = ID(required=True)

    @login_required
    def mutate_and_get_payload(self, info, answer_id, **kwargs):
        credible = kwargs.get("credible", None)
        viewer = info.context.user
        answer_pk = from_global_id(answer_id)[1]
        vote = None
        try:
            vote = Vote.objects.get(user=viewer, answer=answer_pk)
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
                    credible=credible,
                )

        return VoteCreateUpdateDelete(vote=vote)


class Mutation(ObjectType):
    question_create = QuestionCreate.Field()
    answer_create = AnswerCreate.Field()
    vote_create_update_delete = VoteCreateUpdateDelete.Field()
