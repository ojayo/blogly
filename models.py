"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()


def connect_db(app):
    """ Connect to database """
    db.app = app
    db.init_app(app)


class User(db.Model):
    """" User """

    __tablename__ = "users"

    id = db.Column(db.Integer,
    			    primary_key=True,
    			    autoincrement=True)
    first_name = db.Column(db.String(50),
    					    nullable=False)
    last_name = db.Column(db.String(50),
                            nullable=False)
    image_url = db.Column(db.String)

    def __repr__ (self):
        """ show info about user """
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} >"


class Post(db.Model):
    """ Blog post """

    __tablename__ = "posts"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.Text)

    content = db.Column(db.Text)

    # created_at = db.Column(datetime.datetime.now())

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'))

    user = db.relationship('User', backref='posts')


	
