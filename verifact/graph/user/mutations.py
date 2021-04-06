import graphene
from django.contrib.auth.models import User
from graphql_relay import from_global_id
from graphql_jwt.decorators import login_required

from verifact.graph.user.types import UserType
from verifact.graph.scalars import Email


class UserCreate(graphene.relay.ClientIDMutation):
    user = graphene.Field(UserType)

    class Input:
        username = graphene.String(required=True)
        email = Email(required=True)
        password = graphene.String(required=True)

    def mutate_and_get_payload(root, info, username, email, password):
        user = User.objects.create_user(username, email, password)
        return UserCreate(user=user)


class UserUpdate(graphene.relay.ClientIDMutation):
    user = graphene.Field(UserType)

    class Input:
        username = graphene.String()
        email = Email()

    @login_required
    def mutate_and_get_payload(root, info, **input):
        viewer = info.context.user
        username = input.get("username", None)
        email = input.get("email", None)
        if username:
            viewer.username = username
        if email:
            viewer.email = email
        viewer.save()

        return UserUpdate(user=viewer)
