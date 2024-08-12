"""Models for Blogly."""

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
    
    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"

def connect_db(app):
    """Connect this datasbase to provide Flask app.
    
    You should call this in your Flask app.
    """
    db.app = app
    db.init_app(app)
