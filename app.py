import streamlit as st
import random
from time import sleep

def panic_triggered():
    for seconds in range(60):
        with status_container.container():
        # st.write("Panic Button Pressed")
        # sleep(2)
            st.write(f"⏳ {seconds} seconds have passed")
            sleep(1)
    st.write("✔️ 1 minute over!")
    print('Panic button clicked')

def alcohol_detected():
    print('Panic button clicked')

def accident_occured():
    print('Panic button clicked')

st.title("Smart Car with Enhanced Safety System", anchor='title')

status_container = st.empty()

columns = st.columns([2,3])
with columns[0]:
    st.subheader("Simulation Triggers")
    st.button('Panic Button', help="Simulate panic situation", on_click=panic_triggered, args=None, kwargs=None)
    st.button('Alcohol', help="Simulate alcohol detection", on_click=panic_triggered, args=None, kwargs=None)
    st.button('Fake Accident', help="Simulate accident situation", on_click=panic_triggered, args=None, kwargs=None)

with columns[1]:
    st.subheader("Vehicle Parameters")
    st.metric(label="Temperature", value=f"{random.randrange(18,42):4.1f} °C", delta=f"{random.random():3.1f} °C")
    st.metric(label="Humidity", value=f"{random.randrange(18,42):4.1f} °C", delta=f"{random.random():3.1f} °C")
