import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, balanced_accuracy_score
from imblearn.over_sampling import SMOTE

RND = 42
CSV_PATH = "t1.csv"
TARGET_COL = "target"

df = pd.read_csv(CSV_PATH)
feature_cols = [c for c in df.columns if c != TARGET_COL]
X = df[feature_cols].values
y_raw = df[TARGET_COL].values

le = LabelEncoder()
y = le.fit_transform(y_raw)
labels_names = list(le.classes_)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=RND
)

manual_class_weights = [3.0, 1.2, 0.6]
sample_weights = np.array([manual_class_weights[c] for c in y_train])

rf = RandomForestClassifier(
    n_estimators=1000,
    max_depth=30,
    random_state=RND,
    n_jobs=-1
)

rf.fit(X_train, y_train, sample_weight=sample_weights)
y_pred = rf.predict(X_test)

print("=== RandomForest with Manual Class Weights ===")
print("Balanced accuracy:", balanced_accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=labels_names))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))

sm = SMOTE(random_state=RND)
X_train_res, y_train_res = sm.fit_resample(X_train, y_train)

rf_smote = RandomForestClassifier(
    n_estimators=1000,
    max_depth=30,
    random_state=RND,
    n_jobs=-1
)

rf_smote.fit(X_train_res, y_train_res)
y_pred_smote = rf_smote.predict(X_test)

print("\n=== RandomForest with SMOTE ===")
print("Balanced accuracy:", balanced_accuracy_score(y_test, y_pred_smote))
print(classification_report(y_test, y_pred_smote, target_names=labels_names))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred_smote))
