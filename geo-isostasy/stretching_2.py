# streamlit app
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import streamlit as st


st.title("Stretching model - 2")

st.write("""
In this model, the stretched lithosphere is filled with sediments in the
         continental shelf and water in the central part.
         """)

beta = st.number_input("Stretching factor (beta)",
                min_value=1.0,
                max_value=4.0,
                value=2.0,
                step=0.5,
                key="beta")

sed_density = st.number_input("Sediment Density (kg/m^3)",
                min_value=1000,
                max_value=3000,
                value=2400,
                step=50,
                key="filling_density")  

rho_s = sed_density  # kg/m^3
rho_w = 1030  # kg/m^3
rho_c = 2700 # kg/m^3
rho_m = 3300  # kg/m^3

yl = 120 * 1e3
yc = 32 * 1e3

reference_pressure = yc * rho_c + (yl - yc) * rho_m # Pa

def get_ys(rho_fill):
    ys = reference_pressure - (yc / beta) * rho_c - (yl - yc / beta) * rho_m
    ys /= (rho_fill - rho_m)
    return ys

ys = get_ys(rho_s)
yw = get_ys(rho_w)

yas = reference_pressure - ys * rho_s - (yc / beta) * rho_c  - (yl / beta - yc / beta) * rho_m
yas /= rho_m

yaw = reference_pressure - yw * rho_w - (yc / beta) * rho_c  - (yl / beta - yc / beta) * rho_m
yaw /= rho_m

sediment = [0, ys, 0, ys, 0]
water = [0, 0, yw, 0, 0]
crust = [yc, yc / beta, yc / beta, yc / beta, yc]
mantle = [yl - yc , (yl - yc) / beta , (yl - yc) / beta , (yl - yc) / beta, (yl - yc)]
astenosphere = [0, yas, yaw, yas, 0]

st.write(f"Sediment Thickness = {ys:.2f} m - {ys * 3.28084:.2f} ft")
st.write(f"Water Thickness = {yw:.2f} m - {yw * 3.28084:.2f} ft")
rect_width = np.array([1, 1 * beta / 3, 1 * beta / 3, 1 * beta / 3, 1])
total_width = rect_width.sum()
# rect_pos is the sum of the previous widths
rect_pos = [0] + list(np.cumsum(rect_width[:-1])) - total_width / 2

fig, ax = plt.subplots(figsize=(8, 4))

y = np.zeros(5)
for i in range(5):
    ax.add_patch(
        Rectangle((rect_pos[i], y[i]), rect_width[i], astenosphere[i],
                  facecolor="#F53C0E", edgecolor='black', linewidth=0.5))
y += astenosphere

for i in range(5):
    ax.add_patch(Rectangle((rect_pos[i], y[i]), rect_width[i], mantle[i],
                           facecolor="#FFB224", edgecolor='black', linewidth=0.5))

y += mantle

for i in range(5):
    ax.add_patch(Rectangle((rect_pos[i], y[i]), rect_width[i], crust[i],
                           facecolor="#FFF782", edgecolor='black', linewidth=0.5))

y += crust

for i in range(5):
    ax.add_patch(Rectangle((rect_pos[i], y[i]), rect_width[i], sediment[i],
                           facecolor="#144100", edgecolor='black', linewidth=0.5))

y += sediment

for i in range(5):
    ax.add_patch(Rectangle((rect_pos[i], y[i]), rect_width[i], water[i],
                           facecolor="#4DA6FF", edgecolor='black', linewidth=0.5))


ax.set_ylim(0, 130 * 1e3)
ax.set_xlim(-3, 3)

st.pyplot(fig)