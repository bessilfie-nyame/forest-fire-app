import pickle
import numpy as np

MODEL_PATH = 'model/model.sav'
SCALER_PATH = 'model/scaler.pkl'

class AppModel:
    def __init__(self):
        self.__model = None
        self.scaler = None

    def load(self):
        self.__model = pickle.load(open(MODEL_PATH, 'rb'))
        self.scaler = pickle.load(open(SCALER_PATH, 'rb'))
        print("_____Model Loaded Successfully_____")

    def preprocess(self, input_val):
        return self.scaler.transform(input_val) 

    @property
    def model(self):
        return self.__model
