# streamlit app
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import streamlit as st


st.title("Stretching model")

beta = st.number_input("Stretching factor (beta)",
                min_value=1.0,
                max_value=4.0,
                value=2.0,
                step=0.5,
                key="beta")

rho_s = 2400  # kg/m^3
rho_c = 2700 # kg/m^3
rho_m = 3300  # kg/m^3

yl = 120 * 1e3
yc = 32 * 1e3

reference_pressure = yc * rho_c + (yl - yc) * rho_m # Pa

ys = reference_pressure - (yc / beta) * rho_c - (yl - yc / beta) * rho_m
ys /= (rho_s - rho_m)

ya = reference_pressure - ys * rho_s - (yc / beta) * rho_c  - (yl / beta - yc / beta) * rho_m
ya /= rho_m

sediment = [0, ys, 0]
crust = [yc, yc / beta, yc]
mantle = [yl - yc , (yl - yc) / beta, (yl - yc)]
astenosphere = [0, ya, 0]

st.write(f"Sediment Thickness = {ys:.2f} m - {ys * 3.28084:.2f} ft")

rect_width = np.array([1, 1 * beta, 1])
total_width = rect_width.sum()
# rect_pos is the sum of the previous widths
rect_pos = [0] + list(np.cumsum(rect_width[:-1])) - total_width / 2

fig, ax = plt.subplots(figsize=(8, 4))

y = np.zeros(3)
for i in range(3):
    ax.add_patch(
        Rectangle((rect_pos[i], y[i]), rect_width[i], astenosphere[i],
                  facecolor="#F53C0E", edgecolor='black', linewidth=0.5))
y += astenosphere

for i in range(3):
    ax.add_patch(Rectangle((rect_pos[i], y[i]), rect_width[i], mantle[i],
                           facecolor="#FFB224", edgecolor='black', linewidth=0.5))

y += mantle

for i in range(3):
    ax.add_patch(Rectangle((rect_pos[i], y[i]), rect_width[i], crust[i],
                           facecolor="#FFF782", edgecolor='black', linewidth=0.5))

y += crust

for i in range(3):
    ax.add_patch(Rectangle((rect_pos[i], y[i]), rect_width[i], sediment[i],
                           facecolor="#4DA6FF", edgecolor='black', linewidth=0.5))

ax.set_ylim(0, 130 * 1e3)
ax.set_xlim(-3, 3)

st.pyplot(fig)