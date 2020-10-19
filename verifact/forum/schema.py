from graphene import relay, ObjectType, Mutation
from graphene import DateTime, String, Int, Field
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
            created_at=created_at,
            text=text,
            citation_url=citation_url,
            citation_title=citation_title
            if citation_title is not None
            else "Untitled",  # TODO: fetch with OpenGraph if not supplied, or in future more likely implement separate mutations to fetch OpenGraph metadata, then update with OpenGraph metadata if user is happy with it
            citation_image_url=citation_image_url
            if citation_image_url is not None
            else "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Noun_Project_question_mark_icon_1101884_cc.svg/1024px-Noun_Project_question_mark_icon_1101884_cc.svg.png",  # TODO: same as 3 lines up, OpenGraph/metadata retrieval
        )

        question.save()
        return CreateQuestion(question=question)


class CreateAnswer(Mutation):
    class Arguments:
        created_at = DateTime()
        answer = String()
        text = String()
        citation_url = String()
        citation_title = String()
        credible_count = Int()
        not_credible_count = Int()
        question_pk = Int()  # if switching to graphQL ID, switch to String

    answer = Field(AnswerNode)

    def mutate(
        self,
        info,
        answer,
        text,
        question_pk,
        citation_url=None,
        citation_title=None,
        credible_count=0,
        not_credible_count=0,
        created_at=None,
    ):
        answer = Answer.objects.create(
            answer=answer,
            created_at=created_at,
            text=text,
            citation_url=citation_url,
            citation_title=citation_title,
            credible_count=credible_count,
            not_credible_count=not_credible_count,
            question=Question.objects.get(
                pk=question_pk
            ),  # should we use pk or graphQL ID? this uses pk. not sure how to fetch via graphql id though
        )
        answer.save()
        return CreateAnswer(answer=answer)


class Mutation(ObjectType):
    create_question = CreateQuestion.Field()
    create_answer = CreateAnswer.Field()
