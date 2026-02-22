import pandas as pd
import re
from datetime import datetime

# ---------- CONFIG ----------
INPUT_FILE = "data/alcohol_raw.csv"
OUTPUT_FILE = "data/alcohol_clean.csv"
DEFAULT_YEAR = 2025
# ----------------------------

df = pd.read_csv(INPUT_FILE, sep=";")

def parse_date(date_str):
    date_str = str(date_str).strip()

    # Format: 01/01/2025
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except:
        pass

    # Format: 14-feb, 07-mar, etc.
    months = {
        "ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6,
        "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12
    }

    match = re.match(r"(\d{1,2})-([a-zA-Z]+)", date_str.lower())
    if match:
        day = int(match.group(1))
        month_str = match.group(2)[:3]
        month = months.get(month_str, 1)
        return datetime(DEFAULT_YEAR, month, day).strftime("%Y-%m-%d")

    return date_str

df["DATE"] = df["DATE"].apply(parse_date)

def clean_price(price):
    price = str(price).replace("?", "").replace("€", "").strip()
    price = price.replace(",", ".")
    if price == "" or price == "0":
        return 0.00
    return float(price)

df["PRICE"] = df["PRICE"].apply(clean_price)

def clean_text(text):
    if pd.isna(text):
        return ""

    text = str(text).strip()
    text_lower = text.lower()

    exact_replacements = {
        "mahou": "Mahou",
        "vermu": "Vermu",
        "vermú": "Vermu",
        "cafe": "Cafe",
        "caf�": "Cafe",
        "berganti�os": "Bergantinos",
        "jaen": "Jaen",
        "malaga": "Malaga",
        "cadiz": "Cadiz"
    }

    if text_lower in exact_replacements:
        return exact_replacements[text_lower]

    return text.title()

df["DRINK"] = df["DRINK"].apply(clean_text)
df["BRAND"] = df["BRAND"].apply(clean_text)
df["PLACE"] = df["PLACE"].apply(clean_text)

def normalize_brand(brand):
    brand_lower = brand.lower()
    if brand_lower == "estrella":
        return "Estrella Galicia"
    return brand

df["BRAND"] = df["BRAND"].apply(normalize_brand)

def get_location(place):
    place_lower = place.lower()

    malaga_keywords = [
        "malaga", "kali", "tranvia", "seven", "venta",
        "rompeolas", "vox", "galerna", "casa tapia", "casa salas", "anden",
        "zurich", "toros malaga", "feria malaga", "vialia", "casa irene", "casa teresa",
        "casa malaga", "casa navas", "despacho papi", "oleo", "cole", "fomo", "jumanji", "valeria"
    ]

    if any(x in place_lower for x in malaga_keywords):
        return "Malaga"
    elif "manilva" in place_lower:
        return "Manilva"
    elif "madrid" in place_lower:
        return "Madrid"
    elif "jaen" in place_lower:
        return "Jaen"
    elif "cadiz" in place_lower:
        return "Cadiz"
    elif "canarias" in place_lower or "roque nublo" in place_lower:
        return "Canarias"
    elif "marrakech" in place_lower:
        return "Marrakech"
    elif "medjugorje" in place_lower:
        return "Medjugorje"
    elif "cordoba" in place_lower:
        return "Cordoba"
    elif "granada" in place_lower:
        return "Granada"
    elif "jerez" in place_lower:
        return "Jerez"
    elif "el escorial" in place_lower:
        return "El Escorial"
    elif "casa laura" in place_lower:
        return "Moralzarzal"

    return "Madrid"  # default


