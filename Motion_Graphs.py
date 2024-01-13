import streamlit as st
import pandas as pd

accuracy = 0.1
accelerations = dict()

st.title("Motion Graphs")

accuracy = accuracy/int((st.radio("Accuracy",
         ["x1 (Good for preview)", "x10 (Best)", "x100 (Not recommended)"]
         )).split(" ")[0][1:])
st.write(f"Acceleration per {accuracy}s")


st.subheader("Initial Values")
tab_iv1,tab_iv2,tab_iv3,tab_iv4 = st.columns(4)

total_time = tab_iv1.slider('Time', min_value=0, max_value=30, value=15)

try:
    initial_displacement = float(tab_iv2.text_input("Initial Displacement", value=0))
    initial_velocity = float(tab_iv3.text_input("Initial Velocity", value=0))
    initial_acceleration = float(tab_iv4.text_input("Initial Acceleration", value=0))
except ValueError:
    pass

st.subheader("Acceleration Configuration")
num_acce = st.slider('Number of accelerations changed', min_value=1, max_value=10)
t_acc, c_acc = st.columns(2)

acces = []
acce_ts = []

def add_acce(num_acc):
    try:
        with t_acc:
            acce_ts.append(float(st.text_input(label=f"Time changed", key=f"t_acc{num_acc}")))
            
        with c_acc:
            acces.append(float(st.text_input(label=f"Acceleration", key=f"c_acc{num_acc}")))

    except ValueError:
        pass

for i in range(num_acce):
    add_acce(i)
    
data_a = pd.DataFrame(columns=["Time", "Acceleration"])
data_v = pd.DataFrame(columns=["Time", "Velocity"])
data_d = pd.DataFrame(columns=["Time", "Displacement"])
data_merged = pd.DataFrame()   

if st.button(label="Run"):
    with st.spinner("Generating graphs..."):
        data_dic = dict()
        for acc, time in zip(acces, acce_ts):
            data_dic[time] = acc
        
        sec = 0.0
        current_acc = initial_acceleration
        current_velo = initial_velocity
        current_dis = initial_displacement
        while sec <= total_time:
            current_velo += current_acc*accuracy
            current_dis += current_velo*accuracy
            if(sec in data_dic):
                current_acc = data_dic[sec]
            data_a.loc[sec-1] = [sec, current_acc]
            data_v.loc[sec-1] = [sec, current_velo]
            data_d.loc[sec-1] = [sec, current_dis]
            
            sec = round(sec+accuracy, 5)
        
        data_merged = pd.concat([data_a, data_v, data_d], ignore_index=True, axis=1).drop([2,4], axis=1)
        
        data_merged.rename(
            {0: "Time",
             1: "Acceleration",
             2: "",
             3: "Velocity",
             4: "",
             5: "Displacement"
             }
            , axis=1, inplace=True)
        
        st.line_chart(data=data_a, x="Time", y="Acceleration")
        st.line_chart(data=data_v, x="Time", y="Velocity")
        st.line_chart(data=data_d, x="Time", y="Displacement")
        st.line_chart(data=data_merged, x="Time")
        st.write(data_merged)
        
        # st.write("Total Displacement: " + str(round(data_merged["Displacement"].sum()*accuracy, 2)))
