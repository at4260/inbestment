# Purpose: autoload database with u.tickers

import model
from model import User, Rating, Movie
import csv
from datetime import datetime

def load_tickers(session):
    # use u.user
    f = open("./seed_data/u.user")
    # read file and parse using traditional loop method
    for line in f:
        data = line.split("|")
        user_age = data[1]
        user_zipcode = data[4]
        # create new instance of the User class in model.py called my_new_user, set class attributes to variables defined in this function
        my_new_user = User(age=user_age, zipcode=user_zipcode)
        # add each instance to session
        session.add(my_new_user)
    # commit after all instances are added
    session.commit()


def load_prices(session):
    # use u.item
    filename=("./seed_data/u.item")
    # read file and parse using csv method
    with open(filename, 'rb') as csvfile:
        openfile = csv.reader(csvfile, delimiter='|')
        for row in openfile:
            movie_title = row[1]
            # convert latin-1 formatting (with special characters) to unicode, allowing SQLAlchemy to work
            movie_title = movie_title.decode("latin-1")

            # slicing release year out of movie title
            if "(" not in movie_title:
                movie_title = movie_title
            else:
                movie_title = movie_title[:-7]

            movie_release = row[2]
            # convert data to datetime only when release date is not empty; if empty, set to None
            if movie_release != "":
                movie_date = datetime.strptime(movie_release, "%d-%b-%Y")
            else:
                movie_date = None

            # if url doesn't exist, add "" (okay because field is nullable)
            movie_url = row[4]
            my_new_movie = Movie(title=movie_title, release_date=movie_date, url=movie_url)
            session.add(my_new_movie)
        session.commit() 

# def load_ratings(session):
#     # use u.data
#     filename=("./seed_data/u.data")
#     with open(filename, 'rb') as csvfile:
#         openfile = csv.reader(csvfile, delimiter='\t')
#         for row in openfile:
#             rating_user_id = row[0]
#             rating_movie_id = row[1]
#             rating_rating = row[2]
#             my_new_rating = Rating(user_id=rating_user_id, movie_id=rating_movie_id, rating=rating_rating)
#             session.add(my_new_rating)
#         session.commit() 

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    load_movies(session)
    load_ratings(session)

if __name__ == "__main__":
    s= model.connect()
    main(s)
