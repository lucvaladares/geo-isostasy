# streamlit app
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title("Crust and Mantle Thickness Visualization")


rho_m = 3250  # kg/m^3
rho_c = 2700 # kg/m^3
rho_sw = 1030  # kg/m^3

reference_pressure = 35e3 * rho_c + 35e3 * rho_m  # Pa

n_cells = 1000

# input parameters
min_thickness = st.slider("Min Crust Thickness (km)", min_value=0, max_value=50, value=30) * 1e3
max_thickness = st.slider("Max Crust Thickness (km)", min_value=30, max_value=70, value=50) * 1e3

mean_thickness = (min_thickness + max_thickness) / 2

crust = -np.cos(np.linspace(0, 2 * np.pi, n_cells)) * (max_thickness - min_thickness) / 2 + mean_thickness

mantle = (reference_pressure - (rho_c * crust)) / rho_m

mountain_range_size = (crust + mantle).max() - 70e3



st.write(f"Estimated Mountain Range Size: {mountain_range_size:.2f} m")

plt.stackplot(np.arange(n_cells),
              [mantle / 1e3, crust / 1e3],
              labels=['Mantle', 'Crust'],
              colors=["#FFB224", "#FFF782"],
              edgecolor='black',
              linewidth=0.5)
plt.xlim(0, n_cells - 1)
plt.legend(loc='lower right')
plt.grid(alpha=0.3)
plt.ylim(0, 100)
plt.yticks(np.arange(0, 110, 10), labels=np.arange(0, 110, 10) - 70)
plt.xlabel("Distance (arbitrary units)")
plt.ylabel("Thickness (km)")
plt.title("Crust and Mantle Thickness Along a Profile")
st.pyplot(plt)

st.title("Sea level")

min_thickness = st.slider("Min Sea Level Thickness (km)", min_value=0, max_value=50, value=0) * 1e3
max_thickness = st.slider("Max Sea Level Thickness (km)", min_value=0, max_value=10, value=4) * 1e3

sea_level = np.linspace(min_thickness, max_thickness, n_cells)

mantle = np.full(n_cells, 35e3)  # m

crust = 70e3 -mantle - sea_level

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
plt.title("Crust, Mantle, and Sea Level Thickness Along a Profile")
st.pyplot(plt)

pressure = rho_sw * sea_level + rho_c * crust + rho_m * mantle
plt.clf()
plt.plot(np.arange(n_cells), pressure / 1e6)
plt.xlim(0, n_cells - 1)
plt.grid(alpha=0.3)
plt.xlabel("Distance (arbitrary units)")
plt.ylabel("Pressure (MPa)")
plt.title("Pressure at Depth Along a Profile")
st.pyplot(plt)

st.title("Isostatic Adjustment with Sea Level")

target_pressure = reference_pressure - rho_sw * sea_level
# h_c * rho_c + h_m * rho_m = target_pressure
# h_c + h_m + sea_level = 70e3
# h_c * rho_c + (70e3 - sea_level - h_c) * rho_m = target_pressure
h_c = (target_pressure - (70e3 - sea_level) * rho_m) / (rho_c - rho_m)
h_m = 70e3 - sea_level - h_c


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

pressure = rho_sw * sea_level + rho_c * h_c + rho_m * h_m
plt.clf()
plt.plot(np.arange(n_cells), pressure / 1e6)
plt.xlim(0, n_cells - 1)
plt.grid(alpha=0.3)
plt.xlabel("Distance (arbitrary units)")
plt.ylabel("Pressure (MPa)")
plt.title("Pressure at Depth Along a Profile")
st.pyplot(plt)