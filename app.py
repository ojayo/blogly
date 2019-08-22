"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = "whiskey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    """ shows home page """

    return redirect('/users')

@app.route('/users')
def user_page():
    """ shows all users """
    
    users = User.query.all()

    return render_template('users.html', users=users)

@app.route('/users/new', methods=["POST", "GET"])
def handle_new_user():
    """ process the add form and adds a new user """

    if request.method == "GET":
        return render_template('form.html')

    else:
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        image_url = request.form['imageUrl']

        new_user_info = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user_info)
        db.session.commit()

        return redirect('/users')

@app.route("/users/<int:user_id>")
def user_info(user_id):
    """ displays info about the user """

    user = User.query.get(user_id)
    # why can't we do user = User.query.get(1).all()
    # User.query returns a query object
    # you have to pick if you want one or all, can't do both

    return render_template('user-detail.html', user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST", "GET"])
def edit_user(user_id):
    """ edit user information """

    user_info = User.query.get_or_404(user_id)

    if request.method == "GET":
        first_name = user_info.first_name
        last_name = user_info.last_name
        image_url = user_info.image_url

        return render_template('user-edit.html', id=user_id, first_name=first_name, last_name=last_name, image_url=image_url)
    else: 
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        image_url = request.form['image-url']

        user_info.first_name = first_name
        user_info.last_name = last_name
        user_info.image_url = image_url
        
        db.session.add(user_info)
        db.session.commit()

        return redirect('/users')