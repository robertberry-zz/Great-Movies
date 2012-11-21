#!/usr/bin/env python
"""Script for randomly suggesting movies from Roger Ebert's Great Movies list.
"""

import argparse
import random
import pickle

from mechanize import Browser
from bs4 import BeautifulSoup

END_POINT = "http://rogerebert.suntimes.com/apps/pbcs.dll/" + \
    "section?category=greatmovies_fulllist"

MOVIE_SELECTOR = "div.textblock div.classified_blurb div.blurb"

CACHE_PATH = "movies.pickle"

class MoviesCache(object):
    """Local cache of Great Movies list.
    """
    def __init__(self, file_name):
        self.file_name = file_name
        try:
            f = open(file_name, "r")
            self._data = pickle.load(f)
        except IOError, e:
            self.update()
        except EOFError, e:
            self.update()

    def update(self):
        """Update the cache from the Great Movies website.
        """
        self._data = get_movies()
        self.save()
    
    def save(self):
        """Saves the cache.
        """
        f = open(self.file_name, "w")
        pickle.dump(self._data, f)

    @property
    def movies(self):
        """The movies in the cache.
        """
        return self._data

def get_movies():
    """A current list of the movie titles from the website.
    """
    browser = Browser()
    browser.open(END_POINT)
    html = browser.response().read()
    soup = BeautifulSoup(html)
    movies = soup.select(MOVIE_SELECTOR)
    return [m.text for m in movies]

def main():
    parser = argparse.ArgumentParser(description="Suggests movies from " + \
                                         "Roger Ebert's Great Movies list.")
    parser.add_argument("--update", action="store_true", help="Refresh the " + \
                            "local cache of Great Movies.")
    parser.add_argument("-n", default=1, type=int, help="Number of movies " + \
                            "to suggest.")
    args = parser.parse_args()

    cache = MoviesCache(CACHE_PATH)

    if args.update:
        cache.update()
    
    movies = random.sample(cache.movies, args.n)

    for movie in movies:
        print movie

if __name__ == "__main__":
    main()

