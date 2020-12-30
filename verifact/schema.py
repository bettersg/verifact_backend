import graphene
import graphql_jwt

import verifact.forum.schema as ForumSchema


class Query(ForumSchema.Query, graphene.ObjectType):
    node = graphene.relay.Node.Field()


class Mutation(ForumSchema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.relay.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.relay.Verify.Field()
    refresh_token = graphql_jwt.relay.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
