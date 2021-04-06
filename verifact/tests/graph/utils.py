from graphql_jwt.testcases import JSONWebTokenClient


def auth_query(user, *args, **kwargs):
    client = JSONWebTokenClient()
    client.authenticate(user)
    return client.execute(*args, **kwargs)


def no_auth_query(*args, **kwargs):
    client = JSONWebTokenClient()
    return client.execute(*args, **kwargs)
