# drink-with-moderation
This is a recap of all my 2025 drinks. Hope you enjoy!

# 🍻 Alcohol Tracker & Analysis

This project transforms your **drink consumption logs** into meaningful data and insights. It helps you analyze:

- Number of drinks consumed
- Volume of alcohol
- Spending by drink type and location
- Drinking streaks
- Daily trends in alcohol and number of drinks

---

## 📁 Project Structure
```
├── bebidas_raw.csv # Original CSV with raw records
├── data/
│ └── alcohol_clean.csv # Cleaned CSV with additional columns
├── results/ # Folder where analysis results are saved
├── limpiar_bebidas.py # Script to clean and normalize the data
├── analisis_alcohol.py # Script to generate analysis and plots
└── README.md # This file
```

---

## 🧹 Data Cleaning (`limpiar_bebidas.py`)

This script:

- Normalizes drink and brand names  
- Converts prices to float in euros  
- Creates a standardized `LOCATION` column  
- Converts dates to `YYYY-MM-DD` format  
- Adds the following columns:
  - `VOLUME_L` → total liters of drink  
  - `ALCOHOL_L` → liters of pure alcohol  

**Volume and Alcohol Rules:**

| Drink / Type          | Volume (L) | % Alcohol |
|----------------------|------------|-----------|
| Beer (Casa Madrid)    | 0.3        | 5%        |
| Beer (Casa Malaga)    | 0.2        | 5%        |
| Beer (Other)          | 0.33       | 5%        |
| Vermouth              | 0.2        | 15%       |
| Cocktails (Roncola, Gintonic, Aperol, Mojito, Cocktail, etc.) | 0.4 | 12% |
| Wine / Red / White / Cava | 0.15 | 12% |

**Output:** `data/alcohol_clean.csv`

---

## 📊 Analysis (`analisis_alcohol.py`)

Generates a `results/` folder containing:

1. **General Summary**  
   - Total drinks  
   - Drinks by type  
   File: `resumen_general.txt`

2. **Beer Analysis**  
   - Total beers  
   - Total liters consumed  
   - Beers by brand  
   File: `analisis_cervezas.txt`

3. **Analysis by Location**  
   - Number of drinks, liters of alcohol, and total spending per location  
   File: `analisis_ubicacion.csv`

4. **Price Analysis**  
   - Total spending  
   - Average price per drink  
   - Average price by drink type  
   File: `analisis_precios.txt`

5. **Drinking Streaks**  
   - Longest streak drinking / without drinking  
   File: `rachas.txt`

6. **Plots**  
   - Drinks per day → `bebidas_por_dia.png`  
   - Alcohol volume per day → `alcohol_por_dia.png`  

7. **Top 10 Heaviest Drinking Days**  
   File: `top_10_dias_alcohol.csv`

---

## 🚀 How to Use

1. Place your original CSV `bebidas_raw.csv` in the project root.  
2. Run the cleaning script:

```bash
python limpiar_bebidas.py
```
Run the analysis script:

python analisis_alcohol.py

Explore all results in the results/ folder.
