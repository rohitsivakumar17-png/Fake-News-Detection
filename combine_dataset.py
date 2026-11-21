import csv
from pathlib import Path

OUTPUT_FILE = Path(__file__).resolve().parent / "combined_news_dataset.csv"


def find_dataset_files():
    downloads = Path.home() / "Downloads"
    fake_path = None
    true_path = None

    for candidate in downloads.rglob("*.csv"):
        name = candidate.name.lower()
        if "fake" in name and fake_path is None:
            fake_path = candidate
        elif "true" in name and true_path is None:
            true_path = candidate

    return fake_path, true_path


def combine_datasets(fake_csv: Path, true_csv: Path, output_csv: Path):
    fieldnames = ["title", "text", "subject", "date", "label"]
    rows_written = 0
    fake_count = 0
    true_count = 0

    with output_csv.open("w", encoding="utf-8", newline="") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        writer.writeheader()

        with fake_csv.open("r", encoding="utf-8", newline="") as fake_file:
            reader = csv.DictReader(fake_file)
            for row in reader:
                row["label"] = "fake"
                writer.writerow({
                    "title": row.get("title", ""),
                    "text": row.get("text", ""),
                    "subject": row.get("subject", ""),
                    "date": row.get("date", ""),
                    "label": row["label"],
                })
                fake_count += 1
                rows_written += 1

        with true_csv.open("r", encoding="utf-8", newline="") as true_file:
            reader = csv.DictReader(true_file)
            for row in reader:
                row["label"] = "real"
                writer.writerow({
                    "title": row.get("title", ""),
                    "text": row.get("text", ""),
                    "subject": row.get("subject", ""),
                    "date": row.get("date", ""),
                    "label": row["label"],
                })
                true_count += 1
                rows_written += 1

    return rows_written, fake_count, true_count


def main():
    fake_path, true_path = find_dataset_files()
    if fake_path is None or true_path is None:
        print("Could not find both Fake.csv and True.csv in Downloads.")
        print(f"Fake.csv found: {fake_path}")
        print(f"True.csv found: {true_path}")
        return

    print(f"Found dataset files:")
    print(f"  Fake: {fake_path}")
    print(f"  True: {true_path}")
    print(f"Writing combined dataset to: {OUTPUT_FILE}")

    total, fake_count, true_count = combine_datasets(fake_path, true_path, OUTPUT_FILE)

    print("\nCombine complete.")
    print(f"  Total rows: {total}")
    print(f"  Fake rows: {fake_count}")
    print(f"  Real rows: {true_count}")
    print(f"  Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
