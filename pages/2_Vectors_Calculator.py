import streamlit as st

st.title("Vector Calculator")

num_vectors = st.slider("Number of Vectors", min_value=2, max_value=10)

name_v, t_mag, t_dir = st.columns(3)
vectors_dict = {}

def add_acce(cur_n_vec):
    with name_v:
        st.write("")
        st.write("")
        st.write(f"v{cur_n_vec} = ")
    
    mag = 0
    try:
        with t_mag:
            mag = float(st.text_input(label=f"Magnitude", key=f"t_mag{cur_n_vec}"))
    except ValueError:
        pass
    
    with t_dir:
        direction = st.text_input(label=f"Direction (Ex: E20W)", key=f"t_dir{cur_n_vec}")
        
    vectors_dict[f"v{cur_n_vec}"] = [mag, direction.replace(" ", "").lower()]
    
for i in range(num_vectors):
    add_acce(i)
    
user_in = st.text_input("Calculator (Only supports + and -)")

if st.button("Calculate"):
    partition = user_in.split(" ")
    for p in partition:
        if p in vectors_dict:
            user_in = user_in.replace(p, str(vectors_dict[p][0]))
    
    st.write(f"{user_in} = {eval(user_in)}")