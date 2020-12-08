import graphene

import verifact.forum.schema as ForumSchema


class Query(ForumSchema.Query, graphene.ObjectType):
    node = graphene.relay.Node.Field()


class Mutation(ForumSchema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
