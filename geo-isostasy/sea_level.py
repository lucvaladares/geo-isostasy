import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Sea Level - Changing Mantle")


min_sea_level = st.number_input("Min Sea Level (km)",
                min_value=0.0,
                max_value=4.0,
                value=0.0,
                step=0.5,
                key="min_sea_level") * 1e3

max_sea_level = st.number_input("Max Sea Level (km)",
                min_value=0.5,
                max_value=7.5,
                value=4.0,
                step=0.5,
                key="max_sea_level") * 1e3


#
# ----------------------------------------------------------------
#


rho_sw = 1030  # kg/m^3
rho_c = 2700 # kg/m^3
rho_m = 3250  # kg/m^3

n_cells = 20
n_cells = n_cells + 1 - n_cells % 2

gaussian = lambda x : np.e ** (- (x)**2 / (2 * 0.25**2))

x_coords = np.linspace(-1, 1, num=n_cells, dtype=float)

sea_level = gaussian(x_coords).round(2) * (max_sea_level - min_sea_level) + min_sea_level

reference_pressure = 35e3 * rho_c + 35e3 * rho_m  # Pa
target_pressure = reference_pressure - rho_sw * sea_level
# h_c * rho_c + h_m * rho_m = target_pressure
# h_c + h_m + sea_level = 70e3
# h_c * rho_c + (70e3 - sea_level - h_c) * rho_m = target_pressure
h_c = (target_pressure - (70e3 - sea_level) * rho_m) / (rho_c - rho_m)
h_m = 70e3 - sea_level - h_c

st.write(f"Difference in thickness = {h_c.max() - h_c.min():.2f} m - {(h_c.max() - h_c.min()) * 3.28084:.2f} ft")

plt.clf()
plt.stackplot(np.arange(n_cells),
                [h_m / 1e3, h_c / 1e3, sea_level / 1e3],
                labels=['Mantle', 'Crust', 'Sea Level'],
                colors=["#FFB224", "#FFF782", "#4DA6FF"],
                edgecolor='black',
                linewidth=0.5)
plt.xlim(0, n_cells - 1)
plt.legend(loc='lower right')
plt.grid(alpha=0.3)
plt.ylim(0, 100)
plt.yticks(np.arange(0, 110, 10), labels=np.arange(0, 110, 10) - 70)
plt.xlabel("Distance (arbitrary units)")
plt.ylabel("Thickness (km)")
plt.title("Crust, Mantle, and Sea Level Thickness Along a Profile (Isostatic Adjustment)")
st.pyplot(plt)