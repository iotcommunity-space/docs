import json
import os

def generate_safe_slug(name):
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

        for product in data:
            if "slug" not in product or not product["slug"]:
                product["slug"] = generate_safe_slug(product["name"])

        f.seek(0)
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.truncate()
        print("✅ Slugs updated for all sensors.")

if __name__ == "__main__":
    update_slugs_in_json()
