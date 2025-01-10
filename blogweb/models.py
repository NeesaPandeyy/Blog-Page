from datetime import datetime
from blogweb import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    """
    Represent a user in a database.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): Unique username of the user.
        email (str): Unique email address of the user.
        profile (str): File of user's profile picture (default profile is 'default.jpg').
        password (str): Hashed password of the user.
        posts (relationship): A list of posts created by the user.


    """
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20) , unique=True , nullable = False)
    email = db.Column(db.String(120) , unique=True , nullable = False)
    profile = db.Column(db.String(20),nullable=False,default='default.jpg')
    password = db.Column(db.String(60),nullable=False)
    posts = db.relationship('Post',backref='author',lazy=True)

    def __repr__(self):
        """
        Returns a string representation of the user object.
        """
        return f"User('{self.username}','{self.email}','{self.profile}')"
    
class Post(db.Model):
    """
    Represents a post created by a user.

    Attributes:
        id (int): Unique identifier for the post.
        title (str): Title of the post.
        date_posted (datetime): The date and time when the post was created.
        content (str): Content of the post.
        user_id (int): Foreign key referencing the user who created the post.
    """
    id = db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100) ,nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        """
        Returns a string representation of the post object.
        """
        return f"Post('{self.title}','{self.date_posted}')"