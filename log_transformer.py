from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np

class LogTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, constant=1):
        self.constant = constant
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return np.log1p(X + self.constant)