def main():
    print("Hello from gdacs-flood-db!")


if __name__ == "__main__":
    import json 
    from pathlib import Path

    DATA_DIR = Path(__file__).parent / "data"
    event1 = "FL-1000049.json"
    event1_path = DATA_DIR / "aois" / event1

    with open(event1_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        print(data['features'][0])