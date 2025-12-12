import pandas as pd
import numpy as np
from sklearn.base import TransformerMixin

# documentation: https://stackoverflow.com/questions/57888291/how-to-properly-pickle-sklearn-pipeline-when-using-custom-transformer

class TransformTimekey(TransformerMixin):   
    def transform(self, X_original, *_):
        X = X_original.copy()
        X['time_key'] = pd.to_datetime(X['time_key'], format='%Y%m%d')
        X['year'] = X['time_key'].apply(lambda row: row.year)
        X['month'] = X['time_key'].apply(lambda row: row.month)
        X['day'] = X['time_key'].apply(lambda row: row.day)
        X['weekday'] = X['time_key'].apply(lambda row: row.weekday())
        X['is_weekend'] = X['weekday'].apply(lambda row: row in (5, 6))
        X['sin_weekday'] = np.sin(2*np.pi*X['weekday']/7)
        X = X.drop(columns='time_key')
        return X
    
    def fit(self, *_):
        return self