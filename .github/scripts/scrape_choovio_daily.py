import requests
from bs4 import BeautifulSoup
import json
import time
import os
import re

# ---------- HELPERS ----------
def read_scraped_urls(file_path="scraped_urls.txt"):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f.readlines())

def append_scraped_url(url, file_path="scraped_urls.txt"):
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(url + "\n")

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
        .replace(" ", "-")
        .replace("--", "-")
        .strip("-")
    )

def append_product_to_json(product, file_path="data_sensors.json"):
    product["slug"] = generate_safe_slug(product["name"])
    if os.path.exists(file_path):
        with open(file_path, "r+", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            data.append(product)
            f.seek(0)
            json.dump(data, f, indent=2, ensure_ascii=False)
    else:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([product], f, indent=2, ensure_ascii=False)

# ---------- SCRAPER ----------
def scrape_product_details(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    data = {
        "url": url,
        "name": soup.find("h1", class_="product_title").text.strip() if soup.find("h1", class_="product_title") else None,
        "sku": None,
        "brand": None,
        "price": None,
        "availability": None,
        "short_description": [],
        "full_description": None,
        "use_cases": [],
        "features": [],
        "specifications": [],
        "resources": {},
        "images": []
    }

    for item in soup.select("div.product_meta span"):
        if "SKU" in item.text:
            sku = item.select_one("span.sku")
            data["sku"] = sku.text.strip() if sku else item.text.replace("SKU:", "").strip()
        if "Brand" in item.text:
            brand = item.select_one("a")
            data["brand"] = brand.text.strip() if brand else item.text.replace("Brand:", "").strip()

    price_elem = soup.select_one("p.price")
    stock_elem = soup.select_one("p.stock")
    if price_elem:
        data["price"] = price_elem.text.strip()
    if stock_elem:
        data["availability"] = stock_elem.text.strip()

    short_ul = soup.select_one("div.woocommerce-product-details__short-description ul")
    if short_ul:
        data["short_description"] = [li.text.strip() for li in short_ul.find_all("li")]

    desc_panel = soup.select_one("div.woocommerce-Tabs-panel--description")
    if desc_panel:
        para = desc_panel.find("p")
        data["full_description"] = para.text.strip() if para else None

        current_section = None
        for tag in desc_panel.find_all(["h4", "p", "ul"]):
            if tag.name == "h4":
                heading = tag.get_text(strip=True).lower()
                if "use case" in heading:
                    current_section = "use_cases"
                elif "feature" in heading:
                    current_section = "features"
                elif any(x in heading for x in ["spec", "mechanic", "power", "battery"]):
                    current_section = "specifications"
                else:
                    current_section = None
            elif tag.name == "p" and current_section:
                text = tag.get_text(strip=True)
                if text:
                    data[current_section].append(text)
            elif tag.name == "ul" and current_section:
                for li in tag.find_all("li"):
                    text = li.get_text(strip=True)
                    if text:
                        data[current_section].append(text)

    for a in soup.select("a[href]"):
        href = a.get("href")
        if href and any(x in href.lower() for x in ["dropbox", "wiki", ".pdf", "manual", "firmware", "datasheet", "guide", "user"]):
            key_name = (
                "User Guide" if "user" in href.lower() else
                "Manual" if "manual" in href.lower() else
                "Firmware" if "firmware" in href.lower() else
                "Datasheet" if "datasheet" in href.lower() else
                "Wiki" if "wiki" in href.lower() else
                "Resource"
            )
            # avoid overwriting keys
            count = sum(1 for k in data["resources"] if key_name in k)
            final_key = f"{key_name} {count+1}" if count else key_name
            data["resources"][final_key] = href

    images = [img.get("src") for img in soup.select("div.woocommerce-product-gallery img") if img.get("src")]
    data["images"] = list(set(images))

    return data

# ---------- MAIN ----------
def run_scraper():
    print("🔍 Fetching product list...")
    product_list_url = "https://www.choovio.com/iot-online-shop/?et_per_page=-1"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(product_list_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    all_links = []
    for a in soup.select("a.woocommerce-LoopProduct-link"):
        link = a.get("href")
        if link and link.startswith("https://www.choovio.com/product/"):
            all_links.append(link)

    all_links = list(dict.fromkeys(all_links))
    print(f"✅ Found {len(all_links)} total products.")

    scraped_urls = read_scraped_urls()
    remaining_links = [url for url in all_links if url not in scraped_urls]
    print(f"🚀 Starting from product {len(scraped_urls)+1} to {len(all_links)}...\n")

    for i, url in enumerate(remaining_links, len(scraped_urls)+1):
        try:
            print(f"📦 Scraping ({i}/{len(all_links)}): {url}")
            product_data = scrape_product_details(url)
            append_product_to_json(product_data)
            append_scraped_url(url)
            time.sleep(1.5)
        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")

    print("\n✅ Done! All products scraped successfully.\n")

if __name__ == "__main__":
    run_scraper()
