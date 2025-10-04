from utils.main import ExoPlanetsClassifier
import os


def get_models_names() -> list[str]:
    models_dirs = os.listdir("models")
    models = []
    for i in range(len(models_dirs)):
        if models_dirs[i].endswith(".joblib"):
            models.append(models_dirs[i].removesuffix(".joblib"))

    return models


def get_models() -> dict[str, ExoPlanetsClassifier]:
    models = {}
    models_dirs = os.listdir("models")
    for i in range(len(models_dirs)):
        if models_dirs[i].endswith(".joblib"):
            model_name = models_dirs[i].removesuffix(".joblib")
            models[model_name] = ExoPlanetsClassifier(
                artifact_path=os.path.join("models", models_dirs[i])
            )
    return models


