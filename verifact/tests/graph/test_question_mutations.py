import pytest
from graphql_jwt.exceptions import PermissionDenied

from verifact.tests import factories
from verifact.tests.fake import fake
from verifact.tests.graph.utils import auth_query, no_auth_query
from verifact.forum.models import Question


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
        "citationUrl": question.citation_url,
        "citationTitle": question.citation_title,
        "citationImageUrl": question.citation_image_url,
    }}
    res = auth_query(
        viewer,
        create_mutation % "text",
        variables=variables,
    )
    assert res.data["questionCreate"]["question"]["text"] == question.text


@pytest.mark.django_db
def test_question_create_when_logged_out_returns_permissions_error():
    question = factories.Question.build()
    variables = {"input": {
        "text": question.text,
        "citationUrl": question.citation_url,
        "citationTitle": question.citation_title,
        "citationImageUrl": question.citation_image_url,
    }}
    res = no_auth_query(
        create_mutation % "text",
        variables=variables,
    )
    assert res.errors[0].message == PermissionDenied.default_message
