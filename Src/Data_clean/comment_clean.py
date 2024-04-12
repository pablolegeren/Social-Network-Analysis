# -*- coding: utf-8 -*-
"""comment_clean.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZNaJfvmZ4Mbwr7wE3sNqkjGN305rMuEa
"""

import pandas as pd

import gender_guesser.detector as gender

import re

reviews = pd.read_csv('CommentDataset_v1.csv')

d = gender.Detector(case_sensitive=False)

def solo_un_nombre(name):
    partes = name.split()
    if len(partes) > 1:
        return partes[0]
    else:
        return name

reviews['first_name'] = reviews['name'].apply(solo_un_nombre)

reviews['gender'] = reviews['first_name'].apply(d.get_gender)
reviews = reviews.drop('first_name', axis=1)
reviews.loc[reviews['name'].isin(['Javier', 'Jesus', 'Jesús', 'João']), 'gender'] = 'male'

reviews.loc[reviews['name'].str.startswith('María'), 'gender'] = 'female'
reviews.loc[reviews['name'].isin(['Glória', 'Mary', 'Rocío', 'Lupe',
                                  'Carol', 'Luz', 'Mary Paule', 'Leslie']), 'gender'] = 'female'


def extraer_numeros(texto):
    numeros = re.findall(r'\d+', texto)
    if numeros:
        return int(numeros[0])
    else:
        return None

reviews['rating'] = reviews['valoracion'].apply(extraer_numeros)

reviews = reviews.drop('valoracion', axis=1)

reviews.to_csv('CommentDataset_cleaned_v1.csv', index=False)