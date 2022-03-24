import pandas as pd
from json import loads
import numpy as np
from pprint import pprint

df = pd.read_csv('csv/movies_raw.csv')


def drop(dataframe, columns):
    return dataframe.drop(columns=columns)


def apply_genres(dataframe):
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
    dataframe.drop(columns='genres')
    return dataframe


def apply_keywords(dataframe):
    unique_keywords = set()

    dataframe['keywords'] = tuple(map(
        lambda jsons: tuple(
            map(lambda json: (json['name'],
                              unique_keywords.add(json['name']))[0],
                loads(jsons))),
        tuple(dataframe['keywords'])))
    print(len(unique_keywords), unique_keywords)


def apply_production_companies(dataframe):
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
            dataframe.drop(columns=i)
    dataframe.drop(columns='production_countries')
    return dataframe


def apply_release_date(dataframe):
    def apply(x):
        return int(x.split('-')[0])

    dataframe = dataframe.fillna('0')
    dataframe['release_date'] = \
        dataframe['release_date'].apply(apply).astype(float)
    return dataframe


df = drop(df, ['homepage', 'id', 'budget', 'original_language',
               'production_companies', 'keywords',
               'revenue', 'original_title',
               ])

df = apply_genres(df)
# TODO разобраться с ключевыми словами
# df = apply_keywords(df)
df = apply_production_companies(df)
df = apply_release_date(df)
df = df[df['status'] == 'Released']
df.to_csv('csv/movies.csv')
