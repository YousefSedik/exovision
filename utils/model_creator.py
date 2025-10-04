import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    balanced_accuracy_score,
)
from imblearn.over_sampling import SMOTE
from utils.constants import Constants


class ExoplanetRandomForestModelGenerator:
    REQUIRED_FEATURES = Constants.FEATURES_REQUIRED_TO_PREDICT

    def __init__(self, csv_paths, target_col="koi_disposition", random_state=42):
        self.csv_paths = csv_paths if isinstance(csv_paths, list) else [csv_paths]
        self.target_col = target_col
        self.random_state = random_state
        self.label_encoder = LabelEncoder()
        self.model = None
        self.labels_names = None
        self.conf_matrix = None
        self.best_params = None
        self.scaler = None
        self.features = Constants.FEATURES_REQUIRED_TO_PREDICT

    def load_and_validate(self):
        dfs = []
        for path in self.csv_paths:
            df = pd.read_csv(path)
            # ensure all required features and target exist
            required_plus_target = set(self.REQUIRED_FEATURES + [self.target_col])
            missing = required_plus_target - set(df.columns)
            if missing:
                raise ValueError(f"File {path} is missing features: {missing}")
            dfs.append(df)
        self.df = pd.concat(dfs, ignore_index=True)
        return self.df

    def preprocess(self):
        # Reorder and select features to match the app's expected order
        self.df = self.df[self.features + [self.target_col]]
        X = self.df[self.features].values
        y_raw = self.df[self.target_col].values
        y = self.label_encoder.fit_transform(y_raw)
        self.labels_names = list(self.label_encoder.classes_)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, stratify=y, random_state=self.random_state
        )

        # Fit scaler on training data and transform
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Handle class imbalance with SMOTE on scaled data
        sm = SMOTE(random_state=self.random_state)
        X_train_res, y_train_res = sm.fit_resample(X_train_scaled, y_train)

        return X_train_res, X_test_scaled, y_train_res, y_test

    def train(self, X_train_res, y_train_res):
        param_dist = {
            "n_estimators": [100, 200, 300],
            "max_depth": [10, 20, None],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4],
        }

        rf = RandomForestClassifier(random_state=self.random_state, n_jobs=-1)

        search = RandomizedSearchCV(
            rf,
            param_distributions=param_dist,
            n_iter=5,
            scoring="balanced_accuracy",
            cv=3,
            random_state=self.random_state,
            verbose=1,
            n_jobs=-1,
        )
        search.fit(X_train_res, y_train_res)
        self.model = search.best_estimator_
        self.best_params = search.best_params_

    def evaluate(self, X_test, y_test):
        y_pred = self.model.predict(X_test)
        acc = balanced_accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, target_names=self.labels_names)
        conf_mat = confusion_matrix(y_test, y_pred)

        self.conf_matrix = conf_mat

        print("\n=== Tuned RandomForest with SMOTE ===")
        print("Best Params:", self.best_params)
        print("Balanced accuracy:", acc)
        print(report)
        print("Confusion matrix:\n", conf_mat)

        return acc, report, conf_mat

    def save(self, output_name, output_dir="models"):
        os.makedirs(output_dir, exist_ok=True)
        joblib.dump(
            {
                "model": self.model,
                "label_encoder": self.label_encoder,
                "confusion_matrix": self.conf_matrix,
                "scaler": self.scaler,
                "features": self.features,
            },
            os.path.join(output_dir, f"{output_name}.joblib"),
        )
        print(f"Artifacts saved to {output_dir}")


