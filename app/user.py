from flask_login import UserMixin

# To make implementing a user class easier, 
# you can inherit from UserMixin, which provides default implementations for the following methods:
# is_authenticated, is_active, is_anonymous, get_id()
class User(UserMixin):
    pass