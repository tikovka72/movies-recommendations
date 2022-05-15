import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class FilmsApi:
    def __init__(self,
                 titles_path='titles.npy',
                 keywords_and_genres_path='keywords_with_genres.npy'):
        self.titles = np.load(titles_path, allow_pickle=True)
        self.keywords_and_genres = np.load(keywords_and_genres_path,
                                           allow_pickle=True)

    def get_film_id_by_title(self, film_title):
        if film_title not in self.titles:
            return None
        return np.where(self.titles == film_title)[0][0]

    def get_similar_films_ids(self, film_id, count=15):
        film_data = self.keywords_and_genres[film_id]

        return np.argsort(cosine_similarity(
            film_data,
            self.keywords_and_genres))[0][-count - 1:-1]

    def get_films_titles_by_ids(self, ids):
        return self.titles[ids]

    def search_films_ids_by_fragment(self, fragment):
        return np.where(
            np.char.find(
                np.char.lower(np.array(self.titles, dtype='<U10')),
                fragment.lower()) >= 0)[0]
