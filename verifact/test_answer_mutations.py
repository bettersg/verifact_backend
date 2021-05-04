import pytest
from graphql_jwt.exceptions import PermissionDenied
from graphql_relay import to_global_id

from verifact.tests import factories
from verifact.tests.fake import fake
from verifact.tests.graph.utils import auth_query, no_auth_query
from verifact.forum.models import Answer


create_mutation = """
    mutation ($input: AnswerCreateInput!) {
      answerCreate(input: $input) {
        answer {
          %s
        }
      }
    }
"""

@pytest.mark.django_db
def test_answer_create_with_valid_input_returns_answer():
    user = factories.User()
    viewer = factories.User()
    question = factories.Question(user=user)
    answer = factories.Answer.build(question=question)
    variables = {"input": {
        "answer": answer.answer,
        "text": answer.text,
        "questionId": to_global_id("QuestionNode", question.id),
    }}
    res = auth_query(
        viewer,
        create_mutation % "text",
        variables=variables,
    )
    assert res.data["answerCreate"]["answer"]["text"] == answer.text
    assert Answer.objects.first() is not None

@pytest.mark.django_db
def test_answer_create_when_logged_out_returns_permissions_error():
    user = factories.User()
    question = factories.Question(user=user)
    answer = factories.Answer.build(question=question)
    variables = {"input": {
        "answer": answer.answer,
        "text": answer.text,
        "questionId": to_global_id("QuestionNode", question.id),
    }}
    res = no_auth_query(
        create_mutation % "text",
        variables=variables,
    )
    assert res.errors[0].message == PermissionDenied.default_message
