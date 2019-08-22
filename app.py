"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post
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

        new_user_info = User(first_name=first_name,
                             last_name=last_name, image_url=image_url)
        db.session.add(new_user_info)
        db.session.commit()

        return redirect('/users')


@app.route("/users/<int:user_id>")
def user_info(user_id):
    """ displays info about the user """

    user = User.query.get_or_404(user_id)

    post = Post.query.filter_by(user_id=user_id)
    # Post.query returns a query object

    return render_template('user-detail.html', user=user, posts=post)


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


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """ deletes a user """

    user_info = User.query.get_or_404(user_id)
    # deleted_user = User.query.delete(user_info)
    # don't do the comment, it doesnt work even by itself
    db.session.delete(user_info)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new', methods=["POST", "GET"])
def handle_new_post(user_id):
    """ process the add post """

    user_info = User.query.get_or_404(user_id)

    if request.method == "GET":
        return render_template('post-new-form.html', user=user_info)

    else:
        title = request.form['title']
        content = request.form['content']

        new_post_info = Post(title=title,
                             content=content, user_id=user_info.id)
        db.session.add(new_post_info)
        db.session.commit()

        return redirect(f"/users/{ user_id }")
        # input variables with single curly brace ( and make it an F string)

@app.route('/')