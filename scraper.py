'''import requests
from bs4 import BeautifulSoup
from database import insert_product, insert_price

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def scrape_amazon(url: str):
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        name = soup.find("span", id="productTitle")
        price = soup.find("span", class_="a-price-whole")
        if name and price:
            return name.get_text(strip=True), float(price.get_text(strip=True).replace(",", ""))
    except Exception as e:
        return None, None
    return None, None

def scrape_flipkart(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    try:
        name = soup.find("span", {"class": "B_NuCI"}).get_text(strip=True)
    except:
        name = "Unknown Flipkart Product"

    try:
        price = soup.find("div", {"class": "_30jeq3 _16Jk6d"}).get_text(strip=True)
        price = float(price.replace("₹", "").replace(",", ""))
    except:
        price = None

    return name, price

def scrape_myntra(url: str):
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        name = soup.find("h1", class_="pdp-name")
        price = soup.find("span", class_="pdp-price")
        if name and price:
            return name.get_text(strip=True), float(price.get_text(strip=True).replace("Rs. ", "").replace(",", ""))
    except Exception:
        return None, None
    return None, None

def scrape_ajio(url: str):
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        name = soup.find("h1", class_="prod-name")
        price = soup.find("div", class_="prod-sp")
        if name and price:
            return name.get_text(strip=True), float(price.get_text(strip=True).replace("₹", "").replace(",", ""))
    except Exception:
        return None, None
    return None, None

def scrape_url(url: str):
    if "amazon" in url:
        site, func = "Amazon", scrape_amazon
    elif "flipkart" in url:
        site, func = "Flipkart", scrape_flipkart
    elif "myntra" in url:
        site, func = "Myntra", scrape_myntra
    elif "ajio" in url:
        site, func = "Ajio", scrape_ajio
    else:
        return None, None

    name, price = func(url)
    if name and price:
        pid = insert_product(url, site, name)
        insert_price(pid, price)
        return name, price
    return None, None
'''
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# Setup Selenium Chrome driver (headless)
def get_driver():
    options = Options()
    options.add_argument("--headless=new")  # new headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

#  AMAZON SCRAPER 
def scrape_amazon(url):
    driver = get_driver()
    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    title = soup.select_one("#productTitle")
    price = soup.select_one(".a-price .a-offscreen")

    if not title or not price:
        return None, None

    name = title.get_text(strip=True)

    # Clean and normalize price
    price_text = price.get_text(strip=True)
    price_num = re.sub(r"[^\d]", "", price_text)  # remove ₹, commas, spaces
    if not price_num:
        return name, None

    price_val = int(price_num)

    # Amazon sometimes returns 100x inflated values → fix
    if price_val > 200000:  
        price_val = price_val // 100

    return name, price_val

#  FLIPKART SCRAPER 
def scrape_flipkart(url):
    driver = get_driver()
    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    title = soup.select_one("span.VU-ZEz")
    price = soup.select_one("div.Nx9bqj.CxhGGd")

    if not title or not price:
        return None, None

    name = title.get_text(strip=True)
    price = clean_price(price.get_text())
    return name, price


#  MYNTRA SCRAPER 
def scrape_myntra(url):
    driver = get_driver()
    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    title = soup.select_one("h1.pdp-title")
    price = soup.select_one("span.pdp-price")

    if not title or not price:
        return None, None

    name = title.get_text(strip=True)
    price = clean_price(price.get_text())
    return name, price


#  AJIO SCRAPER 
def scrape_ajio(url):
    driver = get_driver()
    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    title = soup.select_one("h1.prod-name")
    price = soup.select_one("div.price > span")

    if not title or not price:
        return None, None

    name = title.get_text(strip=True)
    price = clean_price(price.get_text())
    return name, price


#  COMMON HELPERS 
def clean_price(text):
    """Extract digits from price string"""
    text = re.sub(r"[^\d]", "", text)
    return int(text) if text.isdigit() else None


def scrape_url(url):
    if "amazon" in url:
        return scrape_amazon(url)
    elif "flipkart" in url:
        return scrape_flipkart(url)
    elif "myntra" in url:
        return scrape_myntra(url)
    elif "ajio" in url:
        return scrape_ajio(url)
    else:
        return None, None
