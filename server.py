"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template('homepage.html')


@app.route('/users')
def show_user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route('/login')
def show_login_page():
    """Send user to login page"""

    return render_template('login.html')

@app.route('/login-submission', methods=['POST'])
def do_login():

    email = request.form.get('email')
    password = request.form.get('password')

    if check_user_in_db(email):
        if User.query.filter_by(password=password):
            session[email] = password
            flash("Logged in.")
            return redirect('/')
        else:
            flash("Wrong password")
            return redirect("/login-submission")

    else:
        return render_template('homepage.html')
        


def check_user_in_db(email):

    if User.query.filter_by(email=email).first():
        return True

    return False

@app.route('/registration-form')
def open_refistration_form():
    return render_template('registration_form.html')

@app.route('/registration', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    age = int(request.form.get('age'))
    zipcode = request.form.get('zip')

    user = User(email= email, password = password, age=age,
                    zipcode=zipcode)

    db.session.add(user)

    db.session.commit()

    flash("Registration successful.")

    return redirect("/")

@app.route('/logout')
def logout():
    session.clear()

    return redirect('/')


@app.route("/movies")
def show_movies():

    #movies = Movie.query.order_by(Movie.title).all()
    movies = Movie.query.options(db.joinedload('ratings')).order_by(Movie.title).all()
    

    movies_dict = {}

    for movie in movies:

        #movie_ratings_obj = Rating.query.filter_by(movie_id = movie.movie_id).all()
        movie_ratings_obj = movie.ratings
        movie_ratings_lst = []

        [movie_ratings_lst.append(movie_rating.score) for movie_rating in movie_ratings_obj]
        
        movies_dict[movie.title] = [movie.imbd_url, movie_ratings_lst]

    return render_template('all-movies.html', movies_dict=movies_dict)

@app.route('/movie-info')
def show_movie_info():
    movie_title = request.args.get('title')

    print(movie_title)

    return render_template("movie-info.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
