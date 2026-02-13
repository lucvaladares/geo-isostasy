import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Isostatic Adjustment with Sea Level - Fixed Mantle")

st.write("""
In this case, we consider a fixed mantle thickness of 35 km and analyze
how the crust thickness adjusts to maintain isostatic equilibrium as
sea level changes.
         
The reference pressure is calculated based on a 35 km thick crust
and a 35 km thick mantle. The sea level varies along the profile, and we
observe how the crust thickness changes in response to these variations
while keeping the mantle thickness constant.
""")

min_sea_level = st.number_input("Min Sea Level (km)",
                min_value=0.0,
                max_value=4.0,
                value=0.0,
                step=0.5,
                key="min_sea_level") * 1e3

max_sea_level = st.number_input("Max Sea Level (km)",
                min_value=0.5,
                max_value=4.5,
                value=4.0,
                step=0.5,
                key="max_sea_level") * 1e3

#
# ----------------------------------------------------------------
#

rho_sw = 1030  # kg/m^3
rho_c = 2700 # kg/m^3
rho_m = 3250  # kg/m^3

reference_pressure = 35e3 * rho_c + 35e3 * rho_m  # Pa

n_cells = 20
n_cells = n_cells + 1 - n_cells % 2

gaussian = lambda x : np.e ** (- (x)**2 / (2 * 0.25**2))

x_coords = np.linspace(-1, 1, num=n_cells, dtype=float)

mantle = np.full(n_cells, 35e3)  # m

sea_level = gaussian(x_coords).round(2) * (max_sea_level - min_sea_level) + min_sea_level

crust = (reference_pressure - (rho_m * mantle) - (rho_sw * sea_level)) / rho_c

#
# ----------------------------------------------------------------
#

st.write(f"Difference in thickness = {crust.max() - crust.min():.2f} m - {(crust.max() - crust.min()) * 3.28084:.2f} ft")

plt.clf()
plt.stackplot(np.arange(n_cells),
                [mantle / 1e3, crust / 1e3, sea_level / 1e3],
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