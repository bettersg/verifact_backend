import re
from graphql import GraphQLError

from verifact.error_strings import EMAIL_INVALID
from graphene.types import String


class Email(String):
    """Validate an email address"""

    @staticmethod
    def validate(email):
        return True if re.match(r"[^@]+@[^@]+\.[^@]+", email) else False

    @staticmethod
    def parse_value(value):
        if Email.validate(value):
            return value
        raise GraphQLError(EMAIL_INVALID)
