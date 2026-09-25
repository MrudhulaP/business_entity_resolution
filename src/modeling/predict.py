import pandas as pd
import joblib
from src.modeling.train_model import FEATURE_COLS

def predict(feature_df, model_path="models/matcher.pkl", threshold=0.5):
    model = joblib.load(model_path)
    feature_df = feature_df.copy()
    feature_df["score"] = model.predict_proba(feature_df[FEATURE_COLS])[:, 1]
    matched = feature_df[feature_df["score"] >= threshold]

    grouped = matched.groupby("source1_entity_id")["candidate_entity_id"] \
        .apply(lambda x: ",".join(sorted(set(x)))).reset_index()
    grouped.columns = ["source1_entity_id", "matched_entity_ids"]
    return grouped

def fill_all_s1(pred_df, s1_ids):
    all_df = pd.DataFrame({"source1_entity_id": s1_ids})
    merged = all_df.merge(pred_df, on="source1_entity_id", how="left")
    merged["matched_entity_ids"] = merged["matched_entity_ids"].fillna("")
    return merged