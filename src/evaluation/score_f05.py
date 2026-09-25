import pandas as pd

def f05_per_entity(pred_ids: set, true_ids: set) -> float:
    if not true_ids and not pred_ids:
        return 1.0
    if not true_ids and pred_ids:
        return 0.0
    tp = len(pred_ids & true_ids)
    fp = len(pred_ids - true_ids)
    fn = len(true_ids - pred_ids)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    if precision == 0 and recall == 0:
        return 0.0
    return (1.25 * precision * recall) / (0.25 * precision + recall)

def macro_f05(pred_tsv, gt_tsv):
    pred = pd.read_csv(pred_tsv, sep="\t").fillna("")
    gt = pd.read_csv(gt_tsv, sep="\t").fillna("")
    pred_map = dict(zip(pred["source1_entity_id"], pred["matched_entity_ids"]))

    scores = []
    for _, row in gt.iterrows():
        true_ids = set(row["matched_entity_ids"].split(",")) if row["matched_entity_ids"] else set()
        pred_ids_str = pred_map.get(row["source1_entity_id"], "")
        pred_ids = set(pred_ids_str.split(",")) if pred_ids_str else set()
        scores.append(f05_per_entity(pred_ids, true_ids))
    return sum(scores) / len(scores)