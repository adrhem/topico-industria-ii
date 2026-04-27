import csv
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path("<path_to_repo>")
CSV = ROOT / "results.csv"
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)

EVENTS = 1000
SCALE = 1_000_000 / EVENTS # 1M de eventos

rows = []
with CSV.open() as f:
    r = csv.DictReader(f)
    for row in r:
        row["seconds"] = float(row["seconds"])
        row["bytes"] = int(row["bytes"])
        rows.append(row)

PARTICLES = ["e-", "mu-", "gamma"]
BOX_ORDER = ["4_ROOT", "5_NPZ", "6_IMG", "8_MLNPZ", "9_H5"]
BOX_LABEL = {
    "4_ROOT": "(4) ROOT",
    "5_NPZ":  "(5) NPZ",
    "6_IMG":  "(6) IMG",
    "8_MLNPZ":"(8) ML_NPZ",
    "9_H5":   "(9) H5",
}
COLORS = {
    "e-": "#1f77b4", 
    "mu-": "#2ca02c", 
    "gamma": "#d62728"
}


def lookup(part, box):
    for r in rows:
        if r["particle"] == part and r["box"] == box:
            return r
    return None


# Gráfica 1
fig, ax = plt.subplots(figsize=(9, 5))
x = np.arange(len(BOX_ORDER))
w = 0.27
for i, p in enumerate(PARTICLES):
    vals = [lookup(p, b)["seconds"] for b in BOX_ORDER]
    ax.bar(x + (i - 1) * w, vals, w, label=p, color=COLORS[p])
ax.set_xticks(x)
ax.set_xticklabels([BOX_LABEL[b] for b in BOX_ORDER])
ax.set_ylabel("Tiempo (segundos)")
ax.set_title("Tiempo de ejecución por caja - 1,000 eventos")
ax.set_yscale("log")
ax.legend()
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(OUT / "tiempos_1k.png", dpi=130)
plt.close(fig)

# Gráfica 2
fig, ax = plt.subplots(figsize=(9, 5))
for i, p in enumerate(PARTICLES):
    vals = [lookup(p, b)["bytes"] / 1024 / 1024 for b in BOX_ORDER]
    ax.bar(x + (i - 1) * w, vals, w, label=p, color=COLORS[p])
ax.set_xticks(x)
ax.set_xticklabels([BOX_LABEL[b] for b in BOX_ORDER])
ax.set_ylabel("Tamaño de archivo (MB)")
ax.set_title("Tamaño de archivo de salida por caja - 1,000 eventos")
ax.legend()
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(OUT / "tamanos_1k.png", dpi=130)
plt.close(fig)

# Gráfica 3
fig, ax = plt.subplots(figsize=(8, 5))
totals_h = []
for p in PARTICLES:
    secs_total = sum(lookup(p, b)["seconds"] for b in BOX_ORDER)
    totals_h.append(secs_total * SCALE / 3600)
bars = ax.bar(PARTICLES, totals_h, color=[COLORS[p] for p in PARTICLES])
for b, v in zip(bars, totals_h):
    ax.text(b.get_x() + b.get_width()/2, v, f"{v:.1f} h",
            ha="center", va="bottom", fontsize=11)
ax.set_ylabel("Horas estimadas (1 millón de eventos)")
ax.set_title("Tiempo total estimado por partícula para 1M de eventos\n(suma de cajas 4, 5, 6, 8 y 9 - 1 core)")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(OUT / "estimado_horas_1M.png", dpi=130)
plt.close(fig)

# Gráfica 4
fig, ax = plt.subplots(figsize=(8, 5))
totals_gb = []
for p in PARTICLES:
    bytes_total = sum(lookup(p, b)["bytes"] for b in BOX_ORDER)
    totals_gb.append(bytes_total * SCALE / 1024**3)
bars = ax.bar(PARTICLES, totals_gb, color=[COLORS[p] for p in PARTICLES])
for b, v in zip(bars, totals_gb):
    ax.text(b.get_x() + b.get_width()/2, v, f"{v:.1f} GB",
            ha="center", va="bottom", fontsize=11)
ax.set_ylabel("Almacenamiento estimado (GB)")
ax.set_title("Almacenamiento total estimado por partícula para 1M de eventos\n(suma de cajas 4, 5, 6, 8 y 9)")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(OUT / "estimado_gb_1M.png", dpi=130)
plt.close(fig)


# Resumen tabular
def fmt_size(n):
    if n >= 1024**4:
        return f"{n/1024**4:.2f} TB"
    if n >= 1024**3:
        return f"{n/1024**3:.2f} GB"
    if n >= 1024**2:
        return f"{n/1024**2:.2f} MB"
    return f"{n} B"


print("\n==== Por caja (1k) ====")
print("particle | box | secs | MB")
for p in PARTICLES:
    for b in BOX_ORDER:
        r = lookup(p, b)
        print(f"{p:6} | {b:8} | {r['seconds']:8.3f} | {r['bytes']/1024/1024:8.2f}")

print("\n==== Estimado 1M eventos por partícula ====")
print("particle | total_horas | total_GB")
for p in PARTICLES:
    s = sum(lookup(p, b)["seconds"] for b in BOX_ORDER)
    bts = sum(lookup(p, b)["bytes"] for b in BOX_ORDER)
    print(f"{p:6} | {s*SCALE/3600:10.2f} | {bts*SCALE/1024**3:10.2f}")

print("\n==== Total agregado 3 partículas (1M c/u) ====")
S = sum(r["seconds"] for r in rows)
B = sum(r["bytes"] for r in rows)
print(f"Tiempo: {S*SCALE/3600:.2f} h ({S*SCALE/86400:.2f} días)")
print(f"Almacenamiento: {fmt_size(B*SCALE)}")
print(f"\nFiguras guardadas en {OUT}")
