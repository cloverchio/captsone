import pickle

import numpy as np


class PredictionService:

    def __init__(self):
        self.prediction_model = None

    def get_salary_prediction(self, experience):
        """
        Returns a salary estimation given an experience value.
        Loads the predictive model which was trained separately.
        """
        if not self.prediction_model:
            self.prediction_model = pickle.load(open('salary_prediction.pkl', 'rb'))
        experience_values = np.array([experience])
        predictions = self.prediction_model.predict(experience_values)
        return predictions.tolist()
