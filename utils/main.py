from sklearn.preprocessing import LabelEncoder
from schemas.schemas import ModelInputForm
from sklearn.pipeline import Pipeline
from joblib import load
import random


class ExoPlanetsClassifier:

    def __init__(self, artifact_path):
        artifact = load(artifact_path)
        print(artifact)
        self.model: Pipeline = artifact.get("model")
        self.le: LabelEncoder = artifact.get("label_encoder")
        self.scaler = artifact.get("scaler")
        self.features = artifact.get("features")
        self.confusion_matrix = artifact.get("confusion_matrix")
        assert self.model is not None
        assert self.le is not None

    def predict(self, data: list[float]):
        if self.scaler is not None:
            scaled_data = self.scaler.transform([data])
        else:
            scaled_data = [data]
        y_pred = self.model.predict(scaled_data)
        y_pred = self.le.inverse_transform(y_pred)

        if y_pred[0] == "CONFIRMED":
            return "Confirmed"
        elif y_pred[0] == "CANDIDATE":
            return "Candidate"
        else:
            return "False Positive"

    def __str__(self):
        return f"model features: {self.features} scaler: {self.scaler}"
