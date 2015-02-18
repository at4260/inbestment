""" Autoload database with data.py data """

import model
from model import Ticker, Price
from datetime import datetime
import data

def load_tickers(session):
        name_dict = data.get_ticker_names(data.build_ticker_url(data.ticker_list))

        user_age = data[1]
        user_zipcode = data[4]
        # create new instance of the User class in model.py called my_new_user, set class attributes to variables defined in this function
        new_ticker = Ticker(symbol=user_age, name=user_zipcode)
        # add each instance to session
        session.add(new_ticker)
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


def main(session):
#     # You'll call each of the load_* functions with the session as an argument
    load_tickers(session)
#     # load_movies(session)
#     # load_ratings(session)
#     pass

if __name__ == "__main__":
    s= model.connect()
    main(s)
