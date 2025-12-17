from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os

CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"

options = webdriver.ChromeOptions()

# IMPORTANT for Windows stability
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

assessments = []

def main():
    print("Opening SHL catalog...")
    driver.get(CATALOG_URL)
    time.sleep(5)

    # 🔽 SCROLL to load products (CRITICAL)
    for _ in range(15):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    anchors = driver.find_elements(By.TAG_NAME, "a")
    links = set()

    for a in anchors:
        href = a.get_attribute("href")
        if href and "/solutions/products/" in href and "job" not in href:
            links.add(href)

    print(f"Found {len(links)} potential links")

    for i, link in enumerate(links, 1):
        print(f"[{i}/{len(links)}]")
        scrape_detail(link)

    with open("data/assessments_raw.json", "w", encoding="utf-8") as f:
        json.dump(assessments, f, indent=2)

    print(f"\nSaved {len(assessments)} assessments")
    driver.quit()




def scrape_detail(url):
    driver.get(url)
    time.sleep(2)

    if "Pre-packaged" in driver.page_source:
        return

    try:
        name = driver.find_element(By.TAG_NAME, "h1").text.strip()
    except:
        return

    description = ""
    try:
        description = driver.find_element(By.CLASS_NAME, "product-description").text
    except:
        pass

    assessments.append({
        "name": name,
        "url": url,
        "description": description
    })

    print(f"✔ {name}")


if __name__ == "__main__":
    main()
