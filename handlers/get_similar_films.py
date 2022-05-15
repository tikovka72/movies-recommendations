from fastapi import FastAPI, Request, Response
from base_api import FilmsApi


def get_similar_films(app: FastAPI, films_api: FilmsApi):
    @app.get('/get_similar_films')
    async def get_similar_films_handler(req: Request, res: Response):
        params = dict(req.query_params)
        res.headers["Access-Control-Allow-Origin"] = "*"

        if 'films_ids' not in params:
            return {'status': 'no films ids'}

        try:
            films_ids = list(map(int, params['films_ids'].split(',')))

        except ValueError:
            return {'status': 'bad films ids'}

        similar_ids = films_api.get_similar_films_ids(
            films_ids, int(params.get('count', '10')))

        similar_films = films_api.get_films_titles_by_ids(similar_ids)
        similar_pairs = [{'id': int(film_id), 'title': film_title}
                         for film_id, film_title
                         in zip(similar_ids, similar_films)]

        return {'status': 'ok', 'similar_films': similar_pairs}
