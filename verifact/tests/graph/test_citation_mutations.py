import pytest
from graphql_jwt.exceptions import PermissionDenied
from graphql_relay import to_global_id
import random
from verifact.tests import factories
from verifact.tests.fake import fake
from verifact.tests.graph.utils import auth_query, no_auth_query
from verifact.forum.models import Citation

create_mutation = """
    mutation ($input: CitationCreateInput!){
      citationCreate(input: $input){
        citation {
          %s
        }
      }
    }
"""
# 
# @pytest.mark.django_db
# def test_citation_create_with_valid_input_returns_citation():
#     user = factories.User()
#     viewer = factories.User()
#     question = factories.Question(user=user)
#     answer = factories.Answer(question=question,user=user)
#     parent_type, parent_object = random.choice([("QuestionNode",question),("AnswerNode",answer)])
#
#     citation = factories.Citation.build(user=viewer,parent_object=parent_object)
#     variables = {"input":{
#         "parentId": to_global_id(parent_type,parent_object.id),
#         "citationUrl": citation.citation_url,
#     }}
#
#     res = auth_query(
#         viewer,
#         create_mutation % "citationUrl,citationTitle,citationImageUrl",
#         variables=variables,
#     )
#
#     assert Citation.objects.first() is not None
#     assert res.data["citationCreate"]["citation"]["citationUrl"] == citation.citation_url
#     assert len(res.data["citationCreate"]["citation"]["citationTitle"]) > 0
#     assert len(res.data["citationCreate"]["citation"]["citationImageUrl"]) > 0
#
# @pytest.mark.django_db
# def test_content_create_with_no_citations_returns_error():
#     user = factories.User()
#     viewer = factories.User()
#     question = factories.Question(user=user)
#     answer = factories.Answer(question=question,user=user)
#     parent_type, parent_object = random.choice([("QuestionNode",question),("AnswerNode",answer)])
#
#     citation = factories.Citation.build(user=viewer,parent_object=parent_object)
#     variables = {"input":{
#         "parentId": to_global_id(parent_type,parent_object.id),
#         "citationUrl": citation.citation_url,
#     }}
#
#     res = no_auth_query(
#         create_mutation % "citationUrl,citationTitle,citationImageUrl",
#         variables=variables,
#     )
#
#     assert res.errors[0].message == PermissionDenied.default_message
