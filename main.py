from fastapi import FastAPI
import uvicorn

from base_api import FilmsApi

from handlers import get_similar_films, search_films

app = FastAPI(debug=False)
films_api = FilmsApi()

get_similar_films.get_similar_films(app, films_api)
search_films.search_films(app, films_api)


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
