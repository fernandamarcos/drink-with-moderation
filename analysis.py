import pandas as pd
import matplotlib.pyplot as plt
import os

# ---------------- CONFIG ----------------
INPUT_FILE = "data/alcohol_clean.csv"
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)
# ----------------------------------------

df = pd.read_csv(INPUT_FILE, sep=";")

df["FECHA"] = pd.to_datetime(df["FECHA"])

# =========================================================
# 1️⃣ ANALISIS GENERAL
# =========================================================

total_bebidas = len(df)
por_tipo = df["BEBIDA"].value_counts()

with open(f"{RESULTS_DIR}/resumen_general.txt", "w") as f:
    f.write(f"Total bebidas: {total_bebidas}\n\n")
    f.write("Bebidas por tipo:\n")
    f.write(por_tipo.to_string())

# =========================================================
# 2️⃣ ANALISIS DETALLADO CERVEZAS
# =========================================================

cervezas = df[df["BEBIDA"].str.lower() == "cerveza"]

cervezas_marca = cervezas["MARCA"].value_counts()
cervezas_total = len(cervezas)
litros_cerveza = cervezas["VOLUMEN_L"].sum()

with open(f"{RESULTS_DIR}/analisis_cervezas.txt", "w") as f:
    f.write(f"Total cervezas: {cervezas_total}\n")
    f.write(f"Litros totales cerveza: {round(litros_cerveza,2)}\n\n")
    f.write("Cervezas por marca:\n")
    f.write(cervezas_marca.to_string())

# =========================================================
# 3️⃣ ANALISIS POR UBICACION
# =========================================================

por_ubicacion = df.groupby("UBICACION").agg({
    "BEBIDA": "count",
    "PRECIO": "sum",
    "ALCOHOL_L": "sum"
}).sort_values("BEBIDA", ascending=False)

por_ubicacion.to_csv(f"{RESULTS_DIR}/analisis_ubicacion.csv", sep=";")

# =========================================================
# 4️⃣ ANALISIS PRECIOS
# =========================================================

precio_total = df["PRECIO"].sum()
precio_medio = df["PRECIO"].mean()
precio_por_tipo = df.groupby("BEBIDA")["PRECIO"].mean()

with open(f"{RESULTS_DIR}/analisis_precios.txt", "w") as f:
    f.write(f"Gasto total: {round(precio_total,2)}\n")
    f.write(f"Precio medio bebida: {round(precio_medio,2)}\n\n")
    f.write("Precio medio por tipo:\n")
    f.write(precio_por_tipo.to_string())

# =========================================================
# 5️⃣ LINE PLOTS
# =========================================================

bebidas_por_dia = df.groupby("FECHA").size()
alcohol_por_dia = df.groupby("FECHA")["ALCOHOL_L"].sum()

# Plot bebidas por dia
plt.figure()
bebidas_por_dia.plot()
plt.title("Numero de bebidas por dia")
plt.xlabel("Fecha")
plt.ylabel("Numero bebidas")
plt.tight_layout()
plt.savefig(f"{RESULTS_DIR}/bebidas_por_dia.png")
plt.close()

# Plot alcohol por dia
plt.figure()
alcohol_por_dia.plot()
plt.title("Litros de alcohol por dia")
plt.xlabel("Fecha")
plt.ylabel("Litros alcohol")
plt.tight_layout()
plt.savefig(f"{RESULTS_DIR}/alcohol_por_dia.png")
plt.close()

# =========================================================
# 6️⃣ RACHAS
# =========================================================

df_dias = df.groupby("FECHA").size().reset_index(name="bebidas")
df_dias = df_dias.set_index("FECHA").asfreq("D", fill_value=0)

racha_bebiendo = 0
racha_sin_beber = 0
max_bebiendo = 0
max_sin_beber = 0

for val in df_dias["bebidas"]:
    if val > 0:
        racha_bebiendo += 1
        racha_sin_beber = 0
    else:
        racha_sin_beber += 1
        racha_bebiendo = 0

    max_bebiendo = max(max_bebiendo, racha_bebiendo)
    max_sin_beber = max(max_sin_beber, racha_sin_beber)

with open(f"{RESULTS_DIR}/rachas.txt", "w") as f:
    f.write(f"Racha mas larga bebiendo: {max_bebiendo} dias\n")
    f.write(f"Racha mas larga sin beber: {max_sin_beber} dias\n")

# =========================================================
# 7️⃣ EXTRA: TOP 10 DIAS MAS INTENSOS
# =========================================================

top_alcohol = alcohol_por_dia.sort_values(ascending=False).head(10)

top_alcohol.to_csv(f"{RESULTS_DIR}/top_10_dias_alcohol.csv")

print("✅ Analisis completo generado en carpeta results/")