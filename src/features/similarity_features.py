import pandas as pd
from rapidfuzz import fuzz
from src.preprocessing.normalize import add_normalized_columns

def jaccard(a: str, b: str) -> float:
    sa, sb = set(a.split()), set(b.split())
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)

def build_features(s1_df, s2_df, s3_df, candidate_df):
    s1_df = add_normalized_columns(s1_df).set_index("entity_id")
    all_other = pd.concat([s2_df, s3_df])
    all_other = add_normalized_columns(all_other).set_index("entity_id")

    rows = []
    for _, r in candidate_df.iterrows():
        s1_id = r["source1_entity_id"]
        if not r["candidate_entity_ids"]:
            continue
        s1_row = s1_df.loc[s1_id]
        for cand_id in r["candidate_entity_ids"].split(","):
            c_row = all_other.loc[cand_id]
            rows.append({
                "source1_entity_id": s1_id,
                "candidate_entity_id": cand_id,
                "name_jaccard": jaccard(s1_row["name_norm"], c_row["name_norm"]),
                "name_token_sort": fuzz.token_sort_ratio(s1_row["name_norm"], c_row["name_norm"]) / 100,
                "name_partial": fuzz.partial_ratio(s1_row["name_norm"], c_row["name_norm"]) / 100,
                "addr_jaccard": jaccard(s1_row["addr_norm"], c_row["addr_norm"]),
                "addr_token_sort": fuzz.token_sort_ratio(s1_row["addr_norm"], c_row["addr_norm"]) / 100,
                "pincode_match": int(s1_row["pincode"] == c_row["pincode"] and s1_row["pincode"] is not None),
                "same_country": int(s1_row["country"] == c_row["country"]),
            })
    return pd.DataFrame(rows)