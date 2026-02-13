# streamlit app
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import matplotlib as mpl

color = "#818181"

mpl.rcParams['axes.titlecolor'] = color
mpl.rcParams['xtick.color'] = color
mpl.rcParams['ytick.color'] = color
mpl.rcParams['axes.edgecolor'] = color
mpl.rcParams['axes.labelcolor'] = color
mpl.rcParams['axes.facecolor'] = "#E6FFFFFF"
mpl.rcParams['figure.facecolor'] = "#BEFFFF00"



pg = st.navigation([
    st.Page("crust_and_mantle.py", title="Crust and Mantle Isostasy"),
    st.Page("sea_level_fixed_mantle.py", title="Sea Level - Fixed Mantle"),
    st.Page("sea_level.py", title="Sea Level - Changing Mantle"),
    st.Page("stretching.py", title="Stretching Model"),
    ])
pg.run()