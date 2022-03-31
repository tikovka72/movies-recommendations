import pandas as pd
from json import loads
import numpy as np
from typing import Sized


def q(question: str) -> bool:
    answer = ''
    while True:
        if answer.lower().strip() in ('yes', 'no', 'y', 'n'):
            return 'y' in answer.lower()
        answer = input(f'{question} - ')


def drop(dataframe: pd.DataFrame,
         columns_to_drop: Sized) -> pd.DataFrame:
    return dataframe.drop(columns=columns_to_drop)


def apply_genres(dataframe: pd.DataFrame) -> (pd.DataFrame, tuple):
    unique_genres = set()

    dataframe['genres'] = tuple(map(
        lambda jsons: tuple(
            map(lambda json: (json['name'],
                              unique_genres.add(json['name']))[0],
                loads(jsons))),
        tuple(dataframe['genres'])))

    dataframe = dataframe.assign(
        **{genre: np.zeros(dataframe.shape[0])
           for genre in list(unique_genres)})

    for i in unique_genres:
        dataframe.loc[
            dataframe['genres'].apply(lambda x: i in x), i] = 1
    dataframe = dataframe.drop(columns='genres')
    return dataframe, tuple(unique_genres)


def apply_keywords(dataframe: pd.DataFrame) -> pd.DataFrame:
    unique_keywords = set()

    dataframe['keywords'] = tuple(map(
        lambda jsons: ';'.join(tuple(
            map(lambda json: (json['name'],
                              unique_keywords.add(json['name']))[0],
                loads(jsons)))),
        tuple(dataframe['keywords'])))

    return dataframe


def apply_production_countries(
        dataframe: pd.DataFrame) -> (pd.DataFrame, tuple):
    unique_production_countries = set()

    dataframe['production_countries'] = tuple(map(
        lambda jsons: tuple(
            map(lambda json:
                (json['name'],
                 unique_production_countries.add(json['name']))[0],
                loads(jsons))),
        tuple(dataframe['production_countries'])))

    dataframe = dataframe.assign(
        **{genre: np.zeros(dataframe.shape[0])
           for genre in list(unique_production_countries)})

    for i in unique_production_countries:
        dataframe.loc[
            dataframe['production_countries'].apply(lambda x: i in x), i] = 1
        if dataframe[i].sum() < 2:
            dataframe = dataframe.drop(columns=i)
    dataframe = dataframe.drop(columns='production_countries')
    return dataframe, tuple(unique_production_countries)


def apply_release_date(dataframe: pd.DataFrame) -> pd.DataFrame:
    def apply(x):
        return int(x.split('-')[0])

    dataframe = dataframe.fillna('0')
    dataframe['release_date'] = \
        dataframe['release_date'].apply(apply).astype(float)
    return dataframe


def main():
    df = pd.read_csv('csv/movies_raw.csv')

    df = drop(df, ['homepage', 'budget', 'original_language',
                   'production_companies',
                   'revenue', 'original_title', 'spoken_languages'
                   ])
    df, genres = apply_genres(df)
    df = apply_keywords(df)
    df, production_countries = apply_production_countries(df)
    df = apply_release_date(df)
    df = df[df['status'] == 'Released']

    if q('Сохранить изменения? (Y/n)'):
        df.to_csv('csv/movies.csv')
        print('Изменения сохранены')


if __name__ == '__main__':
    main()
