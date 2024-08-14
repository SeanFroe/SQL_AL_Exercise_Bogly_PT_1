"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


    # MODELS GO BELOW

class User(db.Model):
    """ User Model"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False,)
    last_name = db.Column(db.String(50),
                          nullable=False)
    image_url = db.Column(db.String(255),
                          nullable=False, default= "https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg" )
   
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"

# PART 2
    
class Post(db.Model):
    """ Post to blog"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text,
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime,
                          nullable="False",
                          default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")

class PostTag(db.Model):
    """ combines Tags and Posts"""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'),
                   primary_key=True)
    tag_id = db.Column(db.Integer,db.ForeignKey('tags.id'),
                       primary_key=True)
    
class Tag(db.Model):
    """Creates Tags"""

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                     nullable=False,)
    
    posts = db.relationship('Post',
                            secondary="posts_tags",
                            # cascade="all,delete",
                            backref="tags",)
    def __repr__(self):
        return f'<Tag id={self.id}: name={self.name}>'

def connect_db(app):
    """Connect this datasbase to provide Flask app.
    
    You should call this in your Flask app.
    """
    db.app = app
    db.init_app(app)