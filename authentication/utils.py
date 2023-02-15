from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class AuthenticateConfirmTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.profile.email_confirmed) + text_type(user.pk) + text_type(timestamp)


class PasswordResetToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.pk) + text_type(timestamp) + text_type(user.profile.reset_password)


confirm_token_generator = AuthenticateConfirmTokenGenerator()
reset_password_generator = PasswordResetToken()
