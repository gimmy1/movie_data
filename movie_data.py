import csv
from collections import defaultdict, namedtuple, Counter

# GLOBALS
MOVIE_DATA = 'movie_metadata.csv'
NUM_TOP_DIRECTORS = 20
MIN_MOVIES = 4
MIN_YEAR = 1960

Movie = namedtuple('Movie', 'title year score')


def get_movies_by_director(csv_file):
    '''Extracts all movies from csv and stores them in a dictionary
    where keys are directors, and values is a list of movies (named tuples)'''
    directors = defaultdict(list)
    with open(csv_file) as data:
        for line in csv.DictReader(data):
            try:
                director = line['director_name']
                title = line['movie_title'].replace('xaO', '')
                year = line['title_year']
                score = line['imdb_score']
            except ValueError:
                continue

            m = Movie(title=title, year=year, score=score)
            directors[director].append(m)

    return directors

directors = get_movies_by_director(MOVIE_DATA)

cnt = Counter()
for director, movies in directors.items():
    cnt[director] += len(movies)

cnt.most_common(5)


def _calc_mean(movies_list):
    """
    Helper method to calculate mean of list of movies
    """
    ratings = [movie.score for movie in movies_list]
    mean = sum(int(ratings)) / max(1, len(ratings))
    return round(mean, 1)

def get_average_scores(directors):
    """
    Filter directors with < MIN_MOVIES and calculate average score
    """
    return { (director, _calc_mean(movies)): movies
            for director, movies in directors.items()
            if len(movies) >= MIN_MOVIES }

directors = get_movies_by_director(MOVIE_DATA)
