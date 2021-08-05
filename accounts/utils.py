from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class AppTokenGenerator(PasswordResetTokenGenerator):
    def __make__hash_value__(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))
    
token_generator = AppTokenGenerator()

