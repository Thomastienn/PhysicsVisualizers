import streamlit as st
import pandas as pd
import numpy as np
import math
import time

st.title("Projectile Motion")

accuracy = 0.1
g = 9.80665

st.subheader("Configuration")
tab1, tab2 = st.columns(2)

initial_height = float(tab1.text_input("Initial Height (m)", value=0))
initial_velocity = float(tab1.text_input("Initial Velocity (m/s)", value=2))

accuracy = accuracy/int((tab2.radio("Accuracy",
         ["x1 (Good for preview)", "x10 (Best)", "x100 (Not recommended)", "x1000 (Scientific Purpose)"]
         )).split(" ")[0][1:])

deg_angle = float(tab2.slider("Angle", min_value=-90, max_value=90, value=0))

def deg_to_rad(degree):
    return degree*math.pi/180

if st.button("Start"):
    with st.spinner("Calculating..."):
        rad_angle = deg_to_rad(deg_angle)
        iv_x = round(math.cos(rad_angle)*initial_velocity, 10)
        iv_y = round(math.sin(rad_angle)*initial_velocity, 10)
        
        t = 0
        cur_h = initial_height
        cur_v = initial_velocity
        distance_x = 0
        distance_y = 0
        cur_dist = 0
        
        displacement_x = 0
        displacement_y = initial_height
        
        displacement = pd.DataFrame(columns=["X", "Y"])
        velocity = pd.DataFrame(columns=["Time", "Velocity"])
        velocity_x = pd.DataFrame(columns=["Time", "Velocity_X"])
        velocity_y = pd.DataFrame(columns=["Time", "Velocity_Y"])
        distance = pd.DataFrame(columns=["Time", "Distance"])
        
        with st.empty():
            while True:
                if(t != 0 and cur_h <= 0):
                    break
                
                distance.loc[t] = [t, cur_dist]
                
                distance_x += (abs(iv_x)*accuracy)
                distance_y += (abs(iv_y)*accuracy)
                
                cur_dist = math.sqrt(distance_x**2 + displacement_y**2)
                
                displacement_x += iv_x*accuracy
                displacement_y += iv_y*accuracy
                
                displacement.loc[t] = [displacement_x, displacement_y]
                velocity.loc[t] = [t, cur_v]
                velocity_x.loc[t] = [t, iv_x]
                velocity_y.loc[t] = [t, iv_y]
                
                cur_h += (iv_y*accuracy)
                iv_y -= (g*accuracy)
                cur_v = math.sqrt(iv_x**2 + iv_y**2)
                t += accuracy
                
                st.write(f"Total Time: {round(t, 5)}")
            
        distance_x = round(distance_x, 5)
        distance_y = round(distance_y, 5)
        
        cur_h = round(cur_h, 5)
        cur_v = round(cur_v, 5)
        iv_y = round(iv_y, 5)
        t = round(t, 5)
        iv_x = round(iv_x, 5)
        
        g_tab1, g_tab2, g_tab3, g_tab4= st.tabs(["Displacement", "Distance", "Velocity", "Summary"])
        
        with g_tab1:
            st.line_chart(data=displacement, x="X", y="Y")
        with g_tab2:
            st.line_chart(data=distance, x="Time", y="Distance")
        with g_tab3:
            st.line_chart(data=velocity, x="Time", y="Velocity")
            st.line_chart(data=velocity_x, x="Time", y="Velocity_X")
            st.line_chart(data=velocity_y, x="Time", y="Velocity_Y")
        with g_tab4:
            st.subheader("Summary")
            st.write(f"Total Time: {t}")
        
        # DEBUG PURPOSES
        # st.write(f"Distance X: {distance_x}", f"Distance Y: {distance_y}", f"Displacement X: {displacement_x}", f"Displacement Y: {displacement_y}", f"Current Height: {cur_h}", f"Total Time: {t}", f"Current Velocity Y: {iv_y}", f"Current Velocity X: {iv_x}")


# with st.empty():
#     for seconds in range(60):
#         st.write(f"⏳ {seconds} seconds have passed")
#         time.sleep(1)   