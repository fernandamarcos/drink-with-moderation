import pandas as pd
import re
from datetime import datetime

# ---------- CONFIG ----------
INPUT_FILE = "data/alcohol_raw.csv"
OUTPUT_FILE = "data/alcohol_clean.csv"
DEFAULT_YEAR = 2025
# ----------------------------

df = pd.read_csv(INPUT_FILE, sep=";")

# ---------- LIMPIAR FECHA ----------
def parse_fecha(fecha):
    fecha = str(fecha).strip()

    # Formato 01/01/2025
    try:
        return datetime.strptime(fecha, "%d/%m/%Y").strftime("%Y-%m-%d")
    except:
        pass

    # Formato 14-feb, 07-mar...
    meses = {
        "ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6,
        "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12
    }

    match = re.match(r"(\d{1,2})-([a-zA-Z]+)", fecha.lower())
    if match:
        dia = int(match.group(1))
        mes_str = match.group(2)[:3]
        mes = meses.get(mes_str, 1)
        return datetime(DEFAULT_YEAR, mes, dia).strftime("%Y-%m-%d")

    return fecha


df["FECHA"] = df["FECHA"].apply(parse_fecha)


# ---------- LIMPIAR PRECIO ----------
def limpiar_precio(precio):
    precio = str(precio).replace("?", "").replace("€", "").strip()
    precio = precio.replace(",", ".")
    if precio == "" or precio == "0":
        return 0.00
    return float(precio)

df["PRECIO"] = df["PRECIO"].apply(limpiar_precio)


# ---------- LIMPIAR TEXTO ----------
def limpiar_texto(texto):
    if pd.isna(texto):
        return ""

    texto = str(texto).strip()
    texto_lower = texto.lower()

    reemplazos_exactos = {
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

    if texto_lower in reemplazos_exactos:
        return reemplazos_exactos[texto_lower]

    return texto.title()


df["BEBIDA"] = df["BEBIDA"].apply(limpiar_texto)
df["MARCA"] = df["MARCA"].apply(limpiar_texto)
df["LUGAR"] = df["LUGAR"].apply(limpiar_texto)


# ---------- NORMALIZAR MARCAS ----------
def normalizar_marca(marca):
    marca_lower = marca.lower()

    if marca_lower == "estrella":
        return "Estrella Galicia"

    return marca

df["MARCA"] = df["MARCA"].apply(normalizar_marca)


# ---------- CREAR UBICACION (SIN TILDES) ----------
def obtener_ubicacion(lugar):
    lugar_lower = lugar.lower()

    # Malaga manual
    if any(x in lugar_lower for x in [
        "malaga", "kali", "tranvia", "seven", "venta",
        "rompeolas", "vox", "galerna", "casa tapia", "casa salas", "anden"
        "zurich", "toros malaga", "feria malaga", "vialia", "casa irene", "casa teresa",
        "casa malaga", "casa navas", "despacho papi", "oleo", "cole", "fomo", "jumanji", "valeria"
    ]):
        return "Malaga"
    if "manilva" in lugar_lower: 
        return "Manilva"

    if "madrid" in lugar_lower:
        return "Madrid"

    if "jaen" in lugar_lower:
        return "Jaen"

    if "cadiz" in lugar_lower:
        return "Cadiz"

    if "canarias" in lugar_lower or "roque nublo" in lugar_lower:
        return "Canarias"

    if "marrakech" in lugar_lower:
        return "Marrakech"

    if "medjugorje" in lugar_lower:
        return "Medjugorje"

    if "cordoba" in lugar_lower:
        return "Cordoba"

    if "granada" in lugar_lower:
        return "Granada"

    if "jerez" in lugar_lower:
        return "Jerez"

    if "el escorial" in lugar_lower:
        return "El Escorial"
    
    if "casa laura" in lugar_lower: 
        return "Moralzarzal"

    return "Madrid"  # default

df["UBICACION"] = df["LUGAR"].apply(obtener_ubicacion)


# ---------- EXPORTAR ----------
df.to_csv(OUTPUT_FILE, sep=";", index=False)

print("✅ Archivo limpio generado:", OUTPUT_FILE)