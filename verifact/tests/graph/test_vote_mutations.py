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
    vote = factories.Vote.build()
    question = factories.Question(user=user)
    answer = factories.Answer(question=question)
    variables = {"input": {
        "answerId": to_global_id("AnswerNode", answer.id),
        "credible": vote.credible,
    }}

    res = auth_query(
        viewer,
        create_mutation % "vote",
        variables=variables,
    )

    assert res.data["voteCreateUpdateDelete"]["vote"]["credible"] == vote.credible
    assert Vote.objects.first() is not None

@pytest.mark.django_db
def test_vote_update_with_valid_input_returns_vote():
    user = factories.User()
    viewer = factories.User()
    vote = factories.Vote.build()
    question = factories.Question(user=user)
    answer = factories.Answer(question=question)
    variables = {"input": {
        "answerId": to_global_id("AnswerNode", answer.id),
        "credible": vote.credible,
    }}

    res = auth_query(
        viewer,
        create_mutation % "vote",
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
        create_mutation % "vote",
        variables=variables,
    )

    assert res2.data["voteCreateUpdateDelete"]["vote"]["created_at"] == vote.created_at
    assert res2.data["voteCreateUpdateDelete"]["vote"]["credible"] != vote.credible
    assert Vote.objects.first() is not None

@pytest.mark.django_db
def test_vote_delete_with_valid_input_returns_none():
    user = factories.User()
    viewer = factories.User()
    vote = factories.Vote.build()
    question = factories.Question(user=user)
    answer = factories.Answer(question=question)
    variables = {"input": {
        "answerId": to_global_id("AnswerNode", answer.id),
        "credible": vote.credible,
    }}

    res = auth_query(
        viewer,
        create_mutation % "vote",
        variables=variables,
    )

    assert res.data["voteCreateUpdateDelete"]["vote"]["credible"] == vote.credible
    assert Vote.objects.first() is not None

    variables2 = {"input": {
        "answerId": to_global_id("AnswerNode", answer.id),
    }}

    res2 = auth_query(
        viewer,
        create_mutation % "vote",
        variables=variables,
    )

    assert res2.data["voteCreateUpdateDelete"]["vote"] == None

    # if attempting to delete a vote that doesn't exist, nothing should happen
    user3 = factories.User()
    viewer3 = factories.User()
    vote3 = factories.Vote.build()
    question3 = factories.Question(user=user3)
    answer3 = factories.Answer(question=question3)
    variables3 = {"input": {
        "answerId": to_global_id("AnswerNode", answer3.id),
    }}

    res3 = auth_query(
        viewer3,
        create_mutation % "vote",
        variables=variables3,
    )

    assert res3.data["voteCreateUpdateDelete"]["vote"] == None


@pytest.mark.django_db
def test_vote_crud_when_logged_out_returns_permissions_error():
    user = factories.User()
    viewer = factories.User()
    question = factories.Question(user=user)
    answer = factories.Answer(question=question)
    vote_credible = random.choice([True,False,None])

    variables = {"input": {
        "answerId": to_global_id("AnswerNode", answer.id),
    }}
    if vote_credible is not None:
        variables["input"]["credible"] = vote_credible

    res = no_auth_query(
        create_mutation % "vote",
        variables=variables,
    )
    assert res.errors[0].message == PermissionDenied.default_message
