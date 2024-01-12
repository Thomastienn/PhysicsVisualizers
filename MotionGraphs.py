import streamlit as st
import pandas as pd

accuracy = 0.1
accelerations = dict()

st.title("Motion Graphs")

accuracy = accuracy/int((st.radio("Accuracy",
         ["x1 (Good for preview)", "x10 (Best)", "x100 (Not recommended)"]
         )).split(" ")[0][1:])
st.write(f"Acceleration per {accuracy}s")

num_acce = st.slider('Number of accelerations changed', min_value=1, max_value=10)
total_time = st.slider('Time', min_value=0, max_value=30, value=15)
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
    
def run():
    with st.spinner("Generating graphs..."):
        data_acceleration = pd.DataFrame(columns=["Time", "Acceleration"])
        data_velocity = pd.DataFrame(columns=["Time", "Velocity"])
        data_displacement = pd.DataFrame(columns=["Time", "Displacement"])
        
        data_dic = dict()
        for acc, time in zip(acces, acce_ts):
            data_dic[time] = acc
        
        sec = 0.0
        current_acc = 0
        current_velo = 0
        current_dis = 0
        while sec <= total_time:
            current_velo += current_acc*accuracy
            current_dis += current_velo*accuracy
            if(sec in data_dic):
                current_acc = data_dic[sec]
            data_acceleration.loc[sec-1] = [sec, current_acc]
            data_velocity.loc[sec-1] = [sec, current_velo]
            data_displacement.loc[sec-1] = [sec, current_dis]
            
            sec = round(sec+accuracy, 5)
        
        data_merged = pd.concat([data_acceleration, data_velocity, data_displacement], ignore_index=True, axis=1).drop([2,4], axis=1)
        
        data_merged.rename(
            {0: "Time",
             1: "Acceleration",
             2: "",
             3: "Velocity",
             4: "",
             5: "Displacement"
             }
            , axis=1, inplace=True)
        
        st.line_chart(data=data_acceleration, x="Time", y="Acceleration")
        st.line_chart(data=data_velocity, x="Time", y="Velocity")
        st.line_chart(data=data_displacement, x="Time", y="Displacement")
        st.line_chart(data=data_merged, x="Time")
        st.write(data_merged)
        
        st.button("Summary", on_click=summary_data)
        
def summary_data():
    st.write("")

run_btn = st.button(label="Run", on_click=run)


