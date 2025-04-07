# 📚 IoT Community Sensor Docs

Welcome to the official repository for [IoTCommunity.Space/docs](https://iotcommunity.space/docs) — a dynamic, fully automated documentation platform for industrial and LoRaWAN sensors.

This repo is powered by:
- 🔄 Daily scraping of [Choovio IoT store](https://www.choovio.com/iot-online-shop/)
- 🧠 Automatic `slug` generation for clean URLs
- 📝 Markdown-based sensor descriptions
- 🚀 GitHub Actions for continuous sync

---

## 📁 Project Structure
iotcommunity-space/docs/
├── data_sensors.json                # 📋 Main scraped sensor dataset with metadata & slug
├── scraped_urls.txt                 # ✅ Tracker for which Choovio URLs have been processed

├── docs/
│   └── sensors/                     # 📂 Each folder here represents one sensor (slug-based)
│       ├── dragino-lht65/
│       │   ├── features.md
│       │   ├── full_description.md
│       │   ├── images.json
│       │   ├── resources.md
│       │   └── short_description.md
│       ├── am102-indoor-ambience-monitoring-sensor/
│       │   ├── ...
│       └── ...

---

## 🌐 Live Site

All sensors are browsable at  
📎 [`https://iotcommunity.space/docs`](https://iotcommunity.space/docs)

Each sensor can be viewed at  
📎 `/docs/[slug]`  
Example:  
`/docs/lansitec-uwb-badge-tracker`

---

## 🔧 How It Works

### 1. Scraping

- Choovio product pages are scraped daily
- Sensor metadata is saved in `data_sensors.json`

### 2. Slug Generation

- If a sensor has no `slug`, one is auto-generated from its name (e.g. `"Lansitec UWB"` → `lansitec-uwb`)
- Run manually using:
  ```bash
  python .github/scripts/add_slugs.py
