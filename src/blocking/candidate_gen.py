import argparse
import csv
from collections import defaultdict
from pathlib import Path

from src.blocking.keys import blocking_keys
from src.preprocessing.normalize import extract_pincode, normalize_address, normalize_name

DEFAULT_MAX_BUCKET_SIZE = 200
DEFAULT_MAX_CANDIDATES = 100


def row_keys(row):
    name = normalize_name(row.get("business_name", ""))
    address = normalize_address(row.get("business_address", ""))
    return blocking_keys(name, address, extract_pincode(address))


def add_source(index, path):
    with path.open("r", encoding="utf-8", newline="") as input_file:
        reader = csv.DictReader(input_file, delimiter="\t")
        for row in reader:
            entity_id = row.get("entity_id", "").strip()
            keys = row_keys(row)
            if not entity_id or not keys:
                continue
            for key in keys:
                index[key].append(entity_id)


def write_candidates(source_dir, output_path, max_bucket_size, max_candidates, file_prefix):
    source_dir = Path(source_dir)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    s2_index = defaultdict(list)
    s3_index = defaultdict(list)
    add_source(s2_index, source_dir / f"{file_prefix}_source2.tsv")
    add_source(s3_index, source_dir / f"{file_prefix}_source3.tsv")

    total_candidates = 0
    row_count = 0
    with (source_dir / f"{file_prefix}_source1.tsv").open(
        "r", encoding="utf-8", newline=""
    ) as input_file, output_path.open("w", encoding="utf-8", newline="") as output_file:
        reader = csv.DictReader(input_file, delimiter="\t")
        writer = csv.writer(output_file, delimiter="\t", lineterminator="\n")
        writer.writerow(["source1_entity_id", "candidate_entity_ids"])
        for row in reader:
            entity_id = row.get("entity_id", "").strip()
            keys = row_keys(row)
            candidates = set()
            for key in keys:
                for index in (s2_index, s3_index):
                    bucket = index.get(key, [])
                    if len(bucket) <= max_bucket_size:
                        candidates.update(bucket)
            selected = sorted(candidates)[:max_candidates]
            writer.writerow([entity_id, ",".join(selected)])
            total_candidates += len(selected)
            row_count += 1

    average = total_candidates / row_count if row_count else 0
    print(f"Candidate pairs written to {output_path.as_posix()} with {row_count} rows")
    print(f"Average candidates per entity: {average:.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate bounded ER candidates.")
    parser.add_argument("--source-dir", default="dataset/test")
    parser.add_argument("--output", default="output/candidate_pairs.tsv")
    parser.add_argument("--max-bucket-size", type=int, default=DEFAULT_MAX_BUCKET_SIZE)
    parser.add_argument("--max-candidates", type=int, default=DEFAULT_MAX_CANDIDATES)
    parser.add_argument("--file-prefix", default="test")
    args = parser.parse_args()
    write_candidates(
        args.source_dir,
        args.output,
        args.max_bucket_size,
        args.max_candidates,
        args.file_prefix,
    )
