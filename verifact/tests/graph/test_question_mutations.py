import pytest
from graphql_jwt.exceptions import PermissionDenied
import random

from verifact.tests import factories
from verifact.tests.fake import fake
from verifact.tests.graph.utils import auth_query, no_auth_query
from verifact.forum.models import Question
from verifact import error_strings


create_mutation = """
    mutation ($input: QuestionCreateInput!) {
      questionCreate(input: $input) {
        question {
          %s
        }
      }
    }
"""

@pytest.mark.django_db
def test_question_create_with_valid_input_returns_question():
    viewer = factories.User()
    question = factories.Question.build()
    variables = {"input": {
        "text": question.text,
        "citationUrls": ["https://ogp.me/"] * random.randint(1,3)
    }}
    res = auth_query(
        viewer,
        create_mutation % "text",
        variables=variables,
    )
    assert res.data["questionCreate"]["question"]["text"] == question.text
    assert Question.objects.first() is not None

@pytest.mark.django_db
def test_answer_create_with_no_citations_returns_error():
    viewer = factories.User()
    question = factories.Question.build()
    variables = {"input": {
        "text": question.text,
        "citationUrls": []
    }}
    res = auth_query(
        viewer,
        create_mutation % "text",
        variables=variables,
    )
    assert res.errors[0].message == error_strings.ANSWER_QUESTION_MINIMUM_ONE_CITATION

@pytest.mark.django_db
def test_question_create_when_logged_out_returns_permissions_error():
    question = factories.Question.build()
    variables = {"input": {
        "text": question.text,
        "citationUrls": ["https://ogp.me/"] * random.randint(1,3)
    }}
    res = no_auth_query(
        create_mutation % "text",
        variables=variables,
    )
    assert res.errors[0].message == PermissionDenied.default_message
