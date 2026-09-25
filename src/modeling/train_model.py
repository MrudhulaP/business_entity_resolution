import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
import joblib

FEATURE_COLS = ["name_jaccard","name_token_sort","name_partial",
                 "addr_jaccard","addr_token_sort","pincode_match","same_country"]

def train(labeled_df, model_path="models/matcher.pkl"):
    X = labeled_df[FEATURE_COLS]
    y = labeled_df["label"]
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model = lgb.LGBMClassifier(n_estimators=300, learning_rate=0.05, max_depth=6)
    model.fit(X_train, y_train, eval_set=[(X_val, y_val)])

    joblib.dump(model, model_path)
    print("Model saved to", model_path)
    return model