import pytest
from graphql_jwt.exceptions import PermissionDenied
from graphql_relay import to_global_id
import random

from verifact.tests import factories
from verifact.tests.fake import fake
from verifact.tests.graph.utils import auth_query, no_auth_query
from verifact.forum.models import Vote

create_mutation = """
    mutation ($input: VoteCreateUpdateDeleteInput!){
      voteCreateUpdateDelete(input: $input){
        vote {
          %s
        }
      }
    }
"""

@pytest.mark.django_db
def test_vote_create_with_valid_input_returns_vote():
    user = factories.User()
    viewer = factories.User()
    question = factories.Question(user=user)
    answer = factories.Answer(question=question,user=user)
    vote = factories.Vote(user=user,answer=answer)

    variables = {"input": {
        "answerId": to_global_id("AnswerNode", answer.id),
        "credible": vote.credible,
    }}

    res = auth_query(
        viewer,
        create_mutation % "credible",
        variables=variables,
    )

    assert res.data["voteCreateUpdateDelete"]["vote"]["credible"] == vote.credible
    assert Vote.objects.first() is not None

@pytest.mark.django_db
def test_vote_update_with_valid_input_returns_vote():
    user = factories.User()
    viewer = factories.User()
    question = factories.Question(user=user)
    answer = factories.Answer(question=question,user=user)
    vote = factories.Vote(user=user,answer=answer)

    variables = {"input": {
        "answerId": to_global_id("AnswerNode", answer.id),
        "credible": vote.credible,
    }}

    res = auth_query(
        viewer,
        create_mutation % "createdAt,credible",
        variables=variables,
    )

    assert res.data["voteCreateUpdateDelete"]["vote"]["credible"] == vote.credible
    assert Vote.objects.first() is not None

    variables2 = {"input": {
        "answerId": to_global_id("AnswerNode", answer.id),
        "credible": not vote.credible,
    }}

    res2 = auth_query(
        viewer,
        create_mutation % "createdAt,credible",
        variables=variables2,
    )

    assert res2.data["voteCreateUpdateDelete"]["vote"]["createdAt"] == res.data["voteCreateUpdateDelete"]["vote"]["createdAt"]
    assert res2.data["voteCreateUpdateDelete"]["vote"]["credible"] != res.data["voteCreateUpdateDelete"]["vote"]["credible"]
    assert Vote.objects.first() is not None

@pytest.mark.django_db
def test_vote_delete_with_valid_input_returns_none():
    user = factories.User()
    viewer = factories.User()
    question = factories.Question(user=user)
    answer = factories.Answer(question=question,user=user)
    vote = factories.Vote(user=user,answer=answer)

    variables = {"input": {
        "answerId": to_global_id("AnswerNode", answer.id),
    }}

    res = auth_query(
        viewer,
        create_mutation % "credible",
        variables=variables,
    )

    assert vote is None

@pytest.mark.django_db
def test_vote_crud_when_logged_out_returns_permissions_error():
    user = factories.User()
    viewer = factories.User()
    question = factories.Question(user=user)
    answer = factories.Answer(question=question,user=user)
    vote_credible = random.choice([True,False,None])

    variables = {"input": {
        "answerId": to_global_id("AnswerNode", answer.id),
    }}
    if vote_credible is not None:
        variables["input"]["credible"] = vote_credible

    res = no_auth_query(
        create_mutation % "credible",
        variables=variables,
    )
    assert res.errors[0].message == PermissionDenied.default_message
