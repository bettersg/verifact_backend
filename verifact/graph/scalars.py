import re
from graphql import GraphQLError
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from verifact.error_strings import EMAIL_INVALID, URL_FORMAT_INVALID
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


class Url(String):
    """Validate a url"""

    @staticmethod
    def parse_value(value):
        try:
            URLValidator(value)
            return value
        except ValidationError:
            raise GraphQLError(error_strings.URL_FORMAT_INVALID)
