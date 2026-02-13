# streamlit app
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


st.title("Crust and Mantle Isostasy")

st.write("""Visualization of the thickness of the Earth's crust and mantle
along a profile, considering a reference pressure with 35km of crust.""")


col1, col2 = st.columns(2)

with col1:
    rho_m = st.number_input("Mantle density (kg/m^3)",
                    min_value=3000,
                    max_value=4000,
                    value=3250,
                    step=50,
                    key="rho_m")

    rho_c = st.number_input("Crust density (kg/m^3)",
                    min_value=2650,
                    max_value=3000,
                    value=2700,
                    step=50,
                    key="rho_c")

with col2:
    min_thickness = st.number_input(
        "Min Crust Thickness (km)",
        min_value=0,
        max_value=50,
        value=35) * 1e3
    max_thickness = st.number_input(
        "Max Crust Thickness (km)",
        min_value=30,
        max_value=70,
        value=55) * 1e3

reference_pressure = 35e3 * rho_c + 35e3 * rho_m  # Pa

n_cells = 20
n_cells = n_cells + 1 - n_cells % 2

gaussian = lambda x : np.e ** (- (x)**2 / (2 * 0.25**2))

x_coords = np.linspace(-1, 1, num=n_cells, dtype=float)

crust = gaussian(x_coords).round(2) * (max_thickness - min_thickness) + min_thickness
mantle = (reference_pressure - (rho_c * crust)) / rho_m

mountain_range_size = (crust + mantle).max() - (crust + mantle).min()

colors = ["#FFB224", "#FFF782"]

st.write(f"Estimated Mountain Range Size: {mountain_range_size:.2f} m - {mountain_range_size * 3.28084:.2f} ft")

plt.stackplot(np.arange(n_cells),
            [mantle / 1e3, crust / 1e3],
            labels=['Mantle', 'Crust'],
            colors=colors,
            edgecolor='black',
            linewidth=0.5)
plt.xlim(0, n_cells - 1)
plt.legend(loc='lower right')
plt.grid(alpha=0.2)

def next_tens(x):
    return np.ceil(x/10) * 10

y_max = next_tens((mantle+crust).max() / 1e3)
y_min = next_tens(mantle.min() / 1e3) - 10
plt.ylim(y_min, y_max)
ticks = np.arange(y_min, y_max + 10, 10).round(2)

plt.yticks(ticks, labels=(ticks - 70).round(2))
plt.xlabel("Distance (arbitrary units)")
plt.ylabel("Thickness (km)")
plt.title("Crust and Mantle Thickness Along a Profile")
st.pyplot(plt)

fig, ax = plt.subplots()
bottom = np.zeros(n_cells)

for i, layer in enumerate([mantle, crust]):
    p = ax.bar(np.arange(n_cells), layer / 1e3,  1.0, bottom=bottom,
               color=colors[i],
               linewidth=0.5,
               edgecolor='grey')
    bottom += layer / 1e3

ax.set_title("Crust and Mantle Thickness Along a Profile")
ax.set_xlim(-.5, n_cells - .5)
ax.set_ylim(y_min, y_max)
ax.set_yticks(ticks, labels=(ticks - 70).round(2))
st.pyplot(fig)