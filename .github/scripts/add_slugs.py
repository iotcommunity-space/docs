import json
import os

def generate_safe_slug(name):
    if not name or not isinstance(name, str):
        return None
    return (
        name.lower()
        .replace("–", "-")
        .replace("/", "-")
        .replace("\\", "-")
        .replace("&", "and")
        .replace("’", "")
        .replace("'", "")
        .replace(",", "")
        .replace(".", "")
        .replace(":", "")
        .replace("™", "")
        .replace("®", "")
        .replace("°", "")
        .replace("(", "")
        .replace(")", "")
        .replace("[", "")
        .replace("]", "")
        .replace(" ", "-")
        .replace("--", "-")
        .strip("-")
    )

def update_slugs_in_json(file_path="data_sensors.json"):
    if not os.path.exists(file_path):
        print("❌ File not found.")
        return

    with open(file_path, "r+", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("❌ Invalid JSON file.")
            return

        skipped = 0
        updated = 0

        for product in data:
            name = product.get("name", "")
            if not name or not isinstance(name, str):
                print(f"⚠️  Skipping product with missing/invalid name: {product.get('url', 'no URL')}")
                skipped += 1
                continue

            product["slug"] = generate_safe_slug(name)
            updated += 1

        f.seek(0)
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.truncate()

        print(f"✅ Slugs updated for {updated} sensors.")
        if skipped:
            print(f"⚠️  Skipped {skipped} sensors due to missing name.")

if __name__ == "__main__":
    update_slugs_in_json()
