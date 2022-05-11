from fastapi import FastAPI, Request
from base_api import FilmsApi


def search_films(app: FastAPI, films_api: FilmsApi):
    @app.get('/search_films')
    def search_films_handler(req: Request):
        params = dict(req.query_params)
        if 'fragment' not in params:
            return {'status': 'no fragment'}

        fragment = params['fragment']
        films_ids_by_fragment = \
            films_api.search_films_ids_by_fragment(fragment)
        films_titles = \
            films_api.get_films_titles_by_ids(films_ids_by_fragment)
        films_pairs = [{int(film_id): film_title}
                       for film_id, film_title
                       in zip(films_ids_by_fragment, films_titles)]
        return {'status': 'ok', 'films': films_pairs}
