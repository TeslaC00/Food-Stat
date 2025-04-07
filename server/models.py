from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username):
        super().__init__()
        self.id = username


# class User(UserMixin):
#     def __init__(self, user_doc):
#         super().__init__()
#         self.id = str(user_doc["_id"])
#         self.username = user_doc["username"]
