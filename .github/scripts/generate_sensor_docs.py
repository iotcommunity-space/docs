import os
import json
import re

DOCS_BASE = "docs/sensors"
DATA_JSON = "data_sensors.json"

def slugify(text):
    """Converts text to a lowercase, dash-separated, URL-safe slug."""
    text = text.strip().lower()
    text = re.sub(r"\s+", "-", text)               # Replace spaces with dash
    text = re.sub(r"[^\w\-]", "", text)            # Remove special characters
    return text

def write_md_file(folder, filename, lines):
    """Write list of strings to a Markdown file, skipping None/empty values."""
    safe_lines = [str(line).strip() for line in lines if line and str(line).strip()]
    with open(os.path.join(folder, filename), "w", encoding="utf-8") as f:
        f.write("\n".join(safe_lines) + "\n")

def write_json_file(folder, filename, data):
    """Write JSON data to a file if it's not empty."""
    if data:
        with open(os.path.join(folder, filename), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

def run():
    if not os.path.exists(DATA_JSON):
        print(f"❌ ERROR: {DATA_JSON} not found.")
        return

    with open(DATA_JSON, "r", encoding="utf-8") as f:
        try:
            sensors = json.load(f)
        except json.JSONDecodeError:
            print("❌ ERROR: Failed to parse JSON from data_sensors.json")
            return

    for sensor in sensors:
        name = sensor.get("name", "unknown-sensor")
        slug = slugify(name)
        folder = os.path.join(DOCS_BASE, slug)
        os.makedirs(folder, exist_ok=True)

        write_md_file(folder, "short_description.md", sensor.get("short_description", []))
        write_md_file(folder, "full_description.md", [sensor.get("full_description") or "No description available."])
        write_md_file(folder, "features.md", sensor.get("features", []))
        write_md_file(folder, "resources.md", list(sensor.get("resources", {}).values()))
        write_json_file(folder, "images.json", sensor.get("images", []))

    print("✅ Sensor docs generated successfully.")

if __name__ == "__main__":
    run()
