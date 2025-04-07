import os
import json
import re
import hashlib

DOCS_BASE = "docs/sensors"
DATA_JSON = "data_sensors.json"

def slugify(text):
    return re.sub(r"[^\w-]", "", text.lower().replace(" ", "-"))

def write_md_file(folder, filename, lines):
    if lines:
        with open(os.path.join(folder, filename), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

def write_json_file(folder, filename, data):
    if data:
        with open(os.path.join(folder, filename), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

def run():
    with open(DATA_JSON, "r", encoding="utf-8") as f:
        sensors = json.load(f)

    for sensor in sensors:
        slug = slugify(sensor.get("name", "unknown"))
        folder = os.path.join(DOCS_BASE, slug)
        os.makedirs(folder, exist_ok=True)

        write_md_file(folder, "short_description.md", sensor.get("short_description", []))
        write_md_file(folder, "full_description.md", [sensor.get("full_description", "")])
        write_md_file(folder, "features.md", sensor.get("features", []))
        write_md_file(folder, "resources.md", list(sensor.get("resources", {}).values()))
        write_json_file(folder, "images.json", sensor.get("images", []))

if __name__ == "__main__":
    run()
