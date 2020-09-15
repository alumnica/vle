from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class TokenGenerator(PasswordResetTokenGenerator):
    """
    Generates token to change password
    """
    def _make_hash_value(self, user, timestamp):
        return (
                text_type(user.pk) + six.text_type(timestamp) +
                text_type(user.is_active)
        )


account_activation_token = TokenGenerator()
