import pandas as pd
import re
from datetime import datetime


CLEAN_FILE = "data/alcohol_clean.csv"

df = pd.read_csv(CLEAN_FILE, sep=";")

# ---------- VOLUMEN Y ALCOHOL ----------

def calcular_volumen(row):
    bebida = row["BEBIDA"].lower()
    lugar = row["LUGAR"].lower()

    # CERVEZA
    if "cerveza" in bebida:
        if "casa madrid" in lugar:
            return 0.3
        if "casa malaga" in lugar:
            return 0.2
        return 0.33  # tercio

    # VERMU
    if "vermu" in bebida:
        return 0.2

    # VINO / CAVA / TINTO
    if any(x in bebida for x in ["vino", "tinto", "blanco", "cava"]):
        return 0.15

    # COPAS
    if any(x in bebida for x in [
        "roncola", "gintonic", "aperol",
        "mojito", "cocktail", "baileys",
        "limoncello"
    ]):
        return 0.4

    return 0.0


def calcular_alcohol(row):
    bebida = row["BEBIDA"].lower()
    volumen = row["VOLUMEN_L"]

    # CERVEZA 5%
    if "cerveza" in bebida:
        graduacion = 0.05

    # VERMU 15%
    elif "vermu" in bebida:
        graduacion = 0.15

    # VINO / CAVA 12%
    elif any(x in bebida for x in ["vino", "tinto", "blanco", "cava"]):
        graduacion = 0.12

    # COPAS 12%
    elif any(x in bebida for x in [
        "roncola", "gintonic", "aperol",
        "mojito", "cocktail", "baileys",
        "limoncello"
    ]):
        graduacion = 0.12

    else:
        graduacion = 0.0

    return round(volumen * graduacion, 4)


df["VOLUMEN_L"] = df.apply(calcular_volumen, axis=1)
df["ALCOHOL_L"] = df.apply(calcular_alcohol, axis=1)

df.to_csv(CLEAN_FILE, sep=";", index=False)
