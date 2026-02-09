# streamlit app
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


st.title("Crust and Mantle Isostasy")

st.write("""Visualization of the thickness of the Earth's crust and mantle
along a profile, considering a reference pressure with 35km of crust.""")

rho_m = 3250  # kg/m^3
rho_c = 2700 # kg/m^3
rho_sw = 1030  # kg/m^3

st.write(f"Mantle Density: {rho_m} kg/m^3")
st.write(f"Crust Density: {rho_c} kg/m^3")

reference_pressure = 35e3 * rho_c + 35e3 * rho_m  # Pa

n_cells = 1000

# input parameters
min_thickness = st.slider("Min Crust Thickness (km)", min_value=0, max_value=50, value=30) * 1e3
max_thickness = st.slider("Max Crust Thickness (km)", min_value=30, max_value=70, value=50) * 1e3

mean_thickness = (min_thickness + max_thickness) / 2

crust = -np.cos(np.linspace(0, 2 * np.pi, n_cells)) * (max_thickness - min_thickness) / 2 + mean_thickness

mantle = (reference_pressure - (rho_c * crust)) / rho_m

mountain_range_size = (crust + mantle).max() - (crust + mantle).min()



st.write(f"Estimated Mountain Range Size: {mountain_range_size:.2f} m")

plt.stackplot(np.arange(n_cells),
            [mantle / 1e3, crust / 1e3],
            labels=['Mantle', 'Crust'],
            colors=["#FFB224", "#FFF782"],
            edgecolor='black',
            linewidth=0.5)
plt.xlim(0, n_cells - 1)
plt.legend(loc='lower right')
plt.grid(alpha=0.2)
plt.ylim(0, 100)
plt.yticks(np.arange(0, 110, 10), labels=np.arange(0, 110, 10) - 70)
plt.xlabel("Distance (arbitrary units)")
plt.ylabel("Thickness (km)")
plt.title("Crust and Mantle Thickness Along a Profile")
st.pyplot(plt)