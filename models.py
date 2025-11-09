from flask_login import UserMixin
from extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def get_id(self):
        return str(self.id)  # Ensure it returns a string, as required by Flask-Login
#abvoe code is for models saving in pyhton sql lachemy db it would run on  local but on server it wont when docker gets restarted so we will be using google cloud fire store for db below is the code for it 


# from google.cloud import firestore
# from werkzeug.security import generate_password_hash, check_password_hash

# # Initialize Firestore client
# db = firestore.Client()
# users_ref = db.collection("users")


# class User:
#     def __init__(self, email, password_hash=None):
#         self.email = email
#         self.password_hash = password_hash

#     @staticmethod
#     def create_user(email, password):
#         """Signup user and save to Firestore"""
#         pw_hash = generate_password_hash(password)
#         users_ref.document(email).set({
#             "email": email,
#             "password_hash": pw_hash,
#             "created_at": firestore.SERVER_TIMESTAMP
#         })
#         return User(email=email, password_hash=pw_hash)

#     @staticmethod
#     def get_user(email):
#         """Fetch user by email from Firestore"""
#         doc = users_ref.document(email).get()
#         if doc.exists:
#             data = doc.to_dict()
#             return User(email=data["email"], password_hash=data["password_hash"])
#         return None

#     def check_password(self, password):
#         """Verify password hash"""
#         return check_password_hash(self.password_hash, password)
