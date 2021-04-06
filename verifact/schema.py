import graphene
import graphql_jwt
from graphql_jwt.decorators import login_required

from verifact.graph.user.types import UserType
from verifact.graph.user.mutations import UserCreate, UserUpdate
import verifact.forum.schema as ForumSchema


class Query(ForumSchema.Query, graphene.ObjectType):
    node = graphene.relay.Node.Field()
    viewer = graphene.Field(UserType)

    @login_required
    def resolve_viewer(root, info):
        return info.context.user


class Mutation(ForumSchema.Mutation, graphene.ObjectType):
    user_create = UserCreate.Field()
    user_update = UserUpdate.Field()
    token_auth = graphql_jwt.relay.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.relay.Verify.Field()
    refresh_token = graphql_jwt.relay.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
