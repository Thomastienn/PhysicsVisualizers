import streamlit as st
import math

st.title("Vector Calculator")

num_vectors = st.slider("Number of Vectors", min_value=2, max_value=10)

t_mag, t_dir = st.columns(2)
vectors_dict = {}

def add_acce(cur_n_vec):
    name_v = f"v{cur_n_vec}"
    
    mag = 0
    try:
        with t_mag:
            mag = float(st.text_input(label=f"Magnitude {name_v}", key=f"t_mag{cur_n_vec}"))
    except ValueError:
        pass
    
    with t_dir:
        direction = st.text_input(label=f"Direction (Ex: E20N)", key=f"t_dir{cur_n_vec}")
        
    vectors_dict[f"v{cur_n_vec}"] = [mag, direction.replace(" ", "").upper()]
    
for i in range(num_vectors):
    add_acce(i)

user_in = st.text_input("Calculator (Only supports + and -) (Ex: -v0 + v1 - v2 + v3)")
user_in = user_in.replace(" ", "").replace("-", " - ").replace("+", " + ")

dir_to_deg = {
    "E": [0, 360],
    "N": [90],
    "W": [180],
    "S": [270]
}

deg_to_dir = {
    0: "E",
    360: "E",
    90: "N",
    180: "W",
    270: "S"
}

SUPPORTED_SYM = ("+", "-")

directions = ["E", "N", "W", "S"]
NUM_OF_DIRECTIONS = len(directions)

def full_dir_to_deg(full_dir):
    if(full_dir in directions):
        return dir_to_deg[full_dir][0]
    
    vector_fixed = full_dir[0]
    vector_arm = full_dir[-1]
    vector_deg = float(full_dir[1:-1])
    
    left_dir_fixed = directions[(directions.index(vector_fixed)+1)%NUM_OF_DIRECTIONS]
    
    v_degree = vector_deg
    if(vector_arm == left_dir_fixed):
        v_degree = dir_to_deg[vector_fixed][0] + vector_deg
    else:
        d_t_d = dir_to_deg[vector_fixed]
        if(vector_fixed == "E"):
            v_degree = d_t_d[1] - vector_deg
        else:
            v_degree = d_t_d[0] - vector_deg
        
    return v_degree

def equal_full_dir(full_dir):
    deg = float(full_dir[1:-1])
    return f"{full_dir[-1]}{round(90-deg, 2)}{full_dir[0]}"

def deg_to_full_dir(deg: float) -> list:
    if deg in deg_to_dir:
        return [deg_to_dir[deg]]
    dir = ""
    while deg > 360:
        deg -= 360
    
    if(0 < deg < 90):
        dir = f"E{deg}N"
    
    elif(90 < deg < 180):
        dir = f"N{deg-90}W"
    
    elif(180 < deg < 270):
        dir = f"W{deg-180}S"
    
    elif(270 < deg < 360):
        dir = f"S{deg-270}E"
        
    return [dir, equal_full_dir(dir)]

def  deg_to_rad(degree):
    return degree*math.pi/180    

def vxy_to_full_dir(v_x,v_y):
    if(v_x == 0):
        v_angle = 0
    else:
        v_angle = abs(round(math.degrees(math.atan(v_y/v_x)), 2))
    
    # Quadrants
    if(v_y > 0 and v_x > 0):
        return f"E{v_angle}N"
    elif(v_y > 0 and v_x < 0):
        return f"N{v_angle}W"
    elif(v_y < 0 and v_x < 0):
        return f"W{v_angle}S"
    elif(v_y < 0 and v_x > 0):
        return f"S{v_angle}E"
    
    # Direct Direction
    if(v_x == 0.0):
        if(v_y > 0):
            return "N"
        return "S"
    if(v_x > 0):
        return "E"
    return "W"
        
    

if st.button("Calculate"):
    partition = user_in.split(" ")
    cur_sym = "+"
    v_xs = []
    v_ys = []
    
    for p in partition:
        if p in vectors_dict:
            vector_direction = vectors_dict[p][1]
            vector_magnitude = vectors_dict[p][0]
            
            if(cur_sym == "-"):
                # vector_direction = deg_to_full_dir(full_dir_to_deg(vector_direction)+180)[0]
                vector_magnitude = -vector_magnitude
                        
            a_vector = vector_direction
            if(len(vector_direction) != 1):
                vector_fixed = vector_direction[0]
                vector_arm = vector_direction[-1]

                left_dir_fixed = directions[(directions.index(vector_fixed)+1)%NUM_OF_DIRECTIONS]
                
                if(vector_arm != left_dir_fixed):
                    a_vector = equal_full_dir(vector_direction)
                
            v_deg = full_dir_to_deg(a_vector)
            
            v_x = (math.cos(deg_to_rad(v_deg)))*vector_magnitude
            v_y = (math.sin(deg_to_rad(v_deg)))*vector_magnitude
            
            v_xs.append(v_x)
            v_ys.append(v_y)
            
        elif p in SUPPORTED_SYM:
            cur_sym = p
    
    vector_x_mag = sum(v_xs)
    vector_y_mag = sum(v_ys)
    
    v_magnitude = math.sqrt(vector_x_mag**2 + vector_y_mag**2)
    
    vector_x_mag = round(vector_x_mag, 5)
    vector_y_mag = round(vector_y_mag, 5)
    
    v_angle = vxy_to_full_dir(vector_x_mag, vector_y_mag)
    st.write(f"{user_in} = {round(v_magnitude,2)} {v_angle} or {equal_full_dir(v_angle)}")