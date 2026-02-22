import pandas as pd
import matplotlib.pyplot as plt
import folium
import os

# ---------------- CONFIG ----------------
INPUT_FILE = "data/alcohol_clean.csv"
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)
# ----------------------------------------

def load_data(file_path):
    df = pd.read_csv(file_path, sep=";")
    df["DATE"] = pd.to_datetime(df["DATE"])
    df["MES"] = df["DATE"].dt.to_period("M").dt.to_timestamp()
    return df

def save_general_analysis(df):
    total_drinks = len(df)
    by_type = df["DRINK"].value_counts()

    with open(f"{RESULTS_DIR}/general_summary.txt", "w") as f:
        f.write(f"Total drinks: {total_drinks}\n\n")
        f.write("Drinks by type:\n")
        f.write(by_type.to_string())

def analyze_beer(df):
    beers = df[df["DRINK"].str.lower() == "cerveza"]
    beer_brands = beers["BRAND"].value_counts()
    total_beers = len(beers)
    total_liters = beers["VOLUMEN_L"].sum()

    with open(f"{RESULTS_DIR}/beer_analysis.txt", "w") as f:
        f.write(f"Total beers: {total_beers}\n")
        f.write(f"Total liters: {round(total_liters,2)}\n\n")
        f.write("Beers by brand:\n")
        f.write(beer_brands.to_string())

def analyze_by_location(df):
    by_location = df.groupby("UBICACION").agg({
        "DRINK": "count",
        "PRICE": "sum",
        "ALCOHOL_L": "sum"
    }).sort_values("DRINK", ascending=False)

    by_location.to_csv(f"{RESULTS_DIR}/location_analysis.csv", sep=";")
    return by_location

def analyze_prices(df):
    total_cost = df["PRICE"].sum()
    mean_price = df["PRICE"].mean()
    mean_price_by_type = df.groupby("DRINK")["PRICE"].mean()

    with open(f"{RESULTS_DIR}/price_analysis.txt", "w") as f:
        f.write(f"Total spending: {round(total_cost,2)}\n")
        f.write(f"Average price per drink: {round(mean_price,2)}\n\n")
        f.write("Average price by drink type:\n")
        f.write(mean_price_by_type.to_string())

def plot_drinks_and_alcohol_over_time(df):
    drinks_per_day = df.groupby("DATE").size()
    alcohol_per_day = df.groupby("DATE")["ALCOHOL_L"].sum()

    plt.figure()
    drinks_per_day.plot()
    plt.title("Number of drinks per day")
    plt.xlabel("Date")
    plt.ylabel("Number of drinks")
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/drinks_per_day.png")
    plt.close()

    plt.figure()
    alcohol_per_day.plot()
    plt.title("Liters of alcohol per day")
    plt.xlabel("Date")
    plt.ylabel("Liters of alcohol")
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/alcohol_per_day.png")
    plt.close()

def plot_monthly_trends(df):
    # Aggregate by month
    monthly = df.groupby("MES").agg({
        "DRINK": "count",
        "ALCOHOL_L": "sum",
        "PRICE": "sum"
    }).rename(columns={
        "DRINK": "TOTAL_DRINKS",
        "ALCOHOL_L": "ALCOHOL_L",
        "PRICE": "SPENDING"
    })

    # Drinks per month
    plt.figure(figsize=(8,5))
    plt.plot(monthly.index, monthly["TOTAL_DRINKS"], marker="o", linewidth=2, color="royalblue")
    plt.title("Total drinks per month")
    plt.xlabel("Month")
    plt.ylabel("Number of drinks")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/line_drinks_per_month.png")
    plt.close()

    # Alcohol per month
    plt.figure(figsize=(8,5))
    plt.plot(monthly.index, monthly["ALCOHOL_L"], marker="o", linewidth=2, color="darkred")
    plt.title("Alcohol consumed per month (L)")
    plt.xlabel("Month")
    plt.ylabel("Liters of alcohol")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/line_alcohol_per_month.png")
    plt.close()

    # Spending per month
    plt.figure(figsize=(8,5))
    plt.plot(monthly.index, monthly["SPENDING"], marker="o", linewidth=2, color="darkgreen")
    plt.title("Money spent per month (€)")
    plt.xlabel("Month")
    plt.ylabel("Euros")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/line_spending_per_month.png")
    plt.close()

def calculate_streaks(df):
    daily_counts = df.groupby("DATE").size().reset_index(name="drinks")
    daily_counts = daily_counts.set_index("DATE").asfreq("D", fill_value=0)

    streak_drinking = streak_no_drinking = max_drinking = max_no_drinking = 0

    for val in daily_counts["drinks"]:
        if val > 0:
            streak_drinking += 1
            streak_no_drinking = 0
        else:
            streak_no_drinking += 1
            streak_drinking = 0
        max_drinking = max(max_drinking, streak_drinking)
        max_no_drinking = max(max_no_drinking, streak_no_drinking)

    with open(f"{RESULTS_DIR}/streaks.txt", "w") as f:
        f.write(f"Longest drinking streak: {max_drinking} days\n")
        f.write(f"Longest dry streak: {max_no_drinking} days\n")

def top_10_drinking_days(df):
    drinks_per_day = df.groupby("DATE").size()
    top_days = drinks_per_day.sort_values(ascending=False).head(10)
    top_days.to_csv(f"{RESULTS_DIR}/top_10_drinking_days.csv")

def plot_drink_type_pie(df, threshold=0.02):
    types = df["DRINK"].value_counts()
    total = types.sum()
    filtered = types[types / total >= threshold]
    others = types[types / total < threshold].sum()
    if others > 0:
        filtered["Others"] = others

    def autopct_format(pct):
        return f"{pct:.1f}%" if pct >= 5 else ""

    plt.figure(figsize=(8,8))
    wedges, texts, autotexts = plt.pie(filtered, autopct=autopct_format, startangle=90)
    plt.legend(wedges, filtered.index, title="Drink Type", loc="center left", bbox_to_anchor=(1, 0.5))
    plt.title("Drink Type Distribution")
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/pie_drink_types.png")
    plt.close()

def plot_beer_brands_pie(df, threshold=0.02):
    beers = df[df["DRINK"].str.lower() == "cerveza"]
    brands = beers["BRAND"].value_counts()
    total = brands.sum()
    filtered = brands[brands / total >= threshold]
    others = brands[brands / total < threshold].sum()
    if others > 0:
        filtered["Others"] = others

    def autopct_format(pct):
        return f"{pct:.1f}%" if pct >= 5 else ""

    plt.figure(figsize=(8,8))
    wedges, texts, autotexts = plt.pie(filtered, autopct=autopct_format, startangle=90)
    plt.legend(wedges, filtered.index, title="Brand", loc="center left", bbox_to_anchor=(1, 0.5))
    plt.title("Beer Brand Distribution")
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/pie_beer_brands.png")
    plt.close()

def plot_top_locations_bar(df, top_n=15):
    top_locations = df["PLACE"].value_counts().head(top_n)
    plt.figure(figsize=(10,6))
    top_locations.sort_values().plot(kind="barh")
    plt.title(f"Top {top_n} drinking locations")
    plt.xlabel("Number of drinks")
    plt.ylabel("Location")
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/bar_top_locations.png")
    plt.close()

def plot_house_locations_bar(df):
    df_house = df[df["PLACE"].str.contains("casa", case=False, na=False)]
    counts = df_house["PLACE"].value_counts()
    plt.figure(figsize=(8,5))
    counts.sort_values().plot(kind="barh")
    plt.title("Number of drinks at friends' houses")
    plt.xlabel("Number of drinks")
    plt.ylabel("House")
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/bar_house_locations.png")
    plt.close()

def create_alcohol_map(df, coords, scale=300):
    mapa = folium.Map(location=[40, -3], zoom_start=6)
    for _, row in df.iterrows():
        location = row["UBICACION"]
        alcohol = row["ALCOHOL_L"]
        if location in coords:
            lat, lon = coords[location]
            folium.Circle(location=(lat, lon),
                          radius=alcohol * scale * 1000,
                          popup=f"{location}\nAlcohol (L): {round(alcohol,2)}",
                          fill=True).add_to(mapa)
    mapa.save(f"{RESULTS_DIR}/alcohol_map.html")

def create_colored_alcohol_map(df, coords):
    def get_color(value, max_value):
        ratio = value / max_value
        if ratio > 0.66:
            return "red"
        elif ratio > 0.33:
            return "orange"
        else:
            return "green"

    # Aggregate by location
    df_grouped = df.groupby("UBICACION").agg({
        "ALCOHOL_L": "sum",
        "PRICE": "sum",
        "DRINK": "count"  # number of drinks
    }).reset_index()

    max_alcohol = df_grouped["ALCOHOL_L"].max()
    mapa = folium.Map(location=[40, -3], zoom_start=6)

    for _, row in df_grouped.iterrows():
        location = row["UBICACION"]
        alcohol = row["ALCOHOL_L"]
        num_drinks = row["DRINK"]
        total_price = row["PRICE"]

        if location in coords:
            lat, lon = coords[location]
            folium.CircleMarker(
                location=(lat, lon),
                radius=10,
                color=get_color(alcohol, max_alcohol),
                fill=True,
                fill_opacity=0.7,
                popup=f"<b>{location}</b><br>"
                      f"Alcohol total: {round(alcohol,2)} L<br>"
                      f"Beverages: {num_drinks}<br>"
                      f"Money: {round(total_price,2)} €"
            ).add_to(mapa)

    mapa.save(f"{RESULTS_DIR}/colored_alcohol_map.html")