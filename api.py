import numpy as np


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


fa = FilmsApi()
print(fa.get_film_id_by_title('Spectre'))