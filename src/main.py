# main.py
import os
import pandas as pd

# Import your modules
import clean_data
import add_info
import analysis

# ---------------- CONFIG ----------------
CLEAN_FILE = "data/alcohol_clean.csv"
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# Coordinates for maps
COORDS = {
    "Madrid": (40.4168, -3.7038),
    "Malaga": (36.7213, -4.4214),
    "Jaen": (37.7796, -3.7849),
    "Moralzarzal": (40.6787, -3.9733),
    "Canarias": (28.2916, -16.6291),
    "Jerez": (36.6850, -6.1261),
    "Granada": (37.1773, -3.5986),
    "Cordoba": (37.8882, -4.7794),
    "Cadiz": (36.5271, -6.2886),
    "Marrakech": (31.6295, -7.9811),
    "Medjugorje": (43.1967, 17.6778),
    "El Escorial": (40.5890, -4.1474),
    "Manilva": (36.3771, -5.2497)
}

def main():
    print("Step 1: Cleaning raw data...")
    clean_data  # this will run your existing clean_data.py and generate alcohol_clean.csv
    print("Data cleaned.")

    print("Step 2: Calculating volume and alcohol...")
    add_info  # this will update CLEAN_FILE with VOLUMEN_L and ALCOHOL_L
    print("Volume and alcohol calculated.")

    print("Step 3: Loading cleaned data...")
    df = pd.read_csv(CLEAN_FILE, sep=";")
    df["DATE"] = pd.to_datetime(df["DATE"])
    df["MES"] = df["DATE"].dt.to_period("M").dt.to_timestamp()
    print("Data loaded.")

    print("Step 4: Running analysis and generating outputs...")
    analysis.save_general_analysis(df)
    analysis.analyze_beer(df)
    analysis.analyze_by_location(df)
    analysis.analyze_prices(df)
    analysis.plot_drinks_and_alcohol_over_time(df)
    analysis.calculate_streaks(df)
    analysis.top_10_drinking_days(df)
    analysis.plot_drink_type_pie(df)
    analysis.plot_beer_brands_pie(df)
    analysis.plot_top_locations_bar(df)
    analysis.plot_house_locations_bar(df)
    analysis.create_alcohol_map(df, COORDS)
    analysis.create_colored_alcohol_map(df, COORDS)
    analysis.plot_monthly_trends(df)
    print("Analysis complete. All outputs saved in 'results/'.")

if __name__ == "__main__":
    main()