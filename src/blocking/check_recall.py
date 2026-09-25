import pandas as pd

def check_recall(candidate_tsv, ground_truth_tsv):
    cand = pd.read_csv(candidate_tsv, sep="\t").fillna("")
    gt = pd.read_csv(ground_truth_tsv, sep="\t").fillna("")

    cand_map = dict(zip(cand["source1_entity_id"], cand["candidate_entity_ids"]))

    total_true_matches = 0
    recovered = 0
    for _, row in gt.iterrows():
        true_ids = set(row["matched_entity_ids"].split(",")) if row["matched_entity_ids"] else set()
        cand_ids = set(cand_map.get(row["source1_entity_id"], "").split(","))
        total_true_matches += len(true_ids)
        recovered += len(true_ids & cand_ids)

    recall = recovered / total_true_matches if total_true_matches else 1.0
    print(f"Blocking recall: {recall:.4f}  ({recovered}/{total_true_matches})")

if __name__ == "__main__":
    check_recall("output/train_candidate_pairs.tsv", "dataset/train/train_ground_truth.tsv")