import pandas as pd

CLEAN_FILE = "data/alcohol_clean.csv"

df = pd.read_csv(CLEAN_FILE, sep=";")

# ---------- VOLUME AND ALCOHOL ----------

def calculate_volume(row):
    drink = row["DRINK"].lower()
    place = row["PLACE"].lower()

    # BEER
    if "cerveza" in drink:
        if "casa madrid" in place:
            return 0.3
        if "casa malaga" in place:
            return 0.2
        return 0.33  # standard bottle

    # VERMU
    if "vermu" in drink:
        return 0.2

    # WINE / CAVA / RED WINE
    if any(x in drink for x in ["vino", "tinto", "blanco", "cava"]):
        return 0.15

    # COCKTAILS / MIXED DRINKS
    if any(x in drink for x in [
        "roncola", "gintonic", "aperol",
        "mojito", "cocktail", "baileys",
        "limoncello", "rebujito"
    ]):
        return 0.4

    return 0.0

def calculate_alcohol(row):
    drink = row["DRINK"].lower()
    volume = row["VOLUMEN_L"]

    # BEER 5%
    if "cerveza" in drink:
        abv = 0.05

    # VERMU 15%
    elif "vermu" in drink:
        abv = 0.15

    # WINE / CAVA 12%
    elif any(x in drink for x in ["vino", "tinto", "blanco", "cava"]):
        abv = 0.12

    # COCKTAILS 12%
    elif any(x in drink for x in [
        "roncola", "gintonic", "aperol",
        "mojito", "cocktail", "baileys",
        "limoncello", "rebujito"
    ]):
        abv = 0.12

    else:
        abv = 0.0

    return round(volume * abv, 4)

# Apply calculations
df["VOLUMEN_L"] = df.apply(calculate_volume, axis=1)
df["ALCOHOL_L"] = df.apply(calculate_alcohol, axis=1)

# Save back to CSV
df.to_csv(CLEAN_FILE, sep=";", index=False)
print("✅ Volume and alcohol calculated, file updated:", CLEAN_FILE)