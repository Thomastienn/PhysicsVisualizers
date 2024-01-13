import streamlit as st

st.title("Projectile Motion")

g = 9.80665
tab1, tab2 = st.columns(2)

initial_height = float(tab1.text_input("Initial Height", value=0))
initial_velocity = float(tab1.text_input("Initial Velocity", value=2))

angle = float(tab2.slider("Angle", min_value=0, max_value=90, value=45))

    
