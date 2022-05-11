from fastapi import FastAPI, Request
from base_api import FilmsApi


def get_similar_films(app: FastAPI, films_api: FilmsApi):
    @app.get('/get_similar_films')
    async def get_similar_films_handler(req: Request):
        params = dict(req.query_params)
        if 'film_name' not in params:
            return {'status': 'no film name'}

        film_id = films_api.get_film_id_by_title(params['film_name'])
        if film_id is None:
            return {'status': 'bad film name'}

        similar_ids = films_api.get_similar_films_ids(
            film_id, int(params.get('count', '15')))

        similar_films = films_api.get_films_titles_by_ids(similar_ids)
        similar_pairs = [{int(film_id): film_title}
                         for film_id, film_title
                         in zip(similar_ids, similar_films)]

        return {'status': 'ok', 'similar_films': similar_pairs}
