import pandas as pd

def label_pairs(feature_df, ground_truth_tsv):
    gt = pd.read_csv(ground_truth_tsv, sep="\t").fillna("")
    match_set = set()
    for _, row in gt.iterrows():
        if row["matched_entity_ids"]:
            for mid in row["matched_entity_ids"].split(","):
                match_set.add((row["source1_entity_id"], mid))

    feature_df = feature_df.copy()
    feature_df["label"] = feature_df.apply(
        lambda r: int((r["source1_entity_id"], r["candidate_entity_id"]) in match_set), axis=1
    )
    return feature_df