from gdacs_flood_db.pipeline import download_all_floods

if __name__ == "__main__":
    total = download_all_floods()
    print(f"Saved {total} flood events")
