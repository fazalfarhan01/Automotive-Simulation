import streamlit as st
import random
from time import sleep
import pandas as pd
import numpy as np


def show_information():
    st.info("Sending information to emergency services.")
    if st.session_state.connectivity:
        with st.spinner('Sending Information...!'):
            sleep(5)
        st.success('Information sent. Emergency services must be on their way.')
        sleep(5)
    else:
        st.warning("Couldn't connect to server.")
        with st.spinner('Initiating peer2peer mode.'):
            sleep(2)
        st.success(f"Connected to nearby node.")
        with st.spinner('Sending info..!'):
            sleep(2)
        st.success('Information sent. Emergency services must be on their way.')
        df = pd.DataFrame([[
            st.session_state.lat, st.session_state.lon
        ]],
        columns=['Latitude', 'Longitude']
        )
        st.table(df)
        sleep(5)


def panic_triggered():
    with status_container.container():
        st.warning("Panic button pressed.")
        show_information()


def alcohol_detected():
    container = status_container.container()
    st.error('Alcohol button clicked')


def accident_occured():
    container = status_container.container()
    st.error('Accident button clicked')


st.title("Smart Car with Enhanced Safety System", anchor='title')

status_container = st.empty()

st.sidebar.subheader("Simulation Triggers")
st.sidebar.button('Panic Button', help="Simulate panic situation",
                  on_click=panic_triggered, args=None, kwargs=None)
st.sidebar.button('Alcohol', help="Simulate alcohol detection",
                  on_click=alcohol_detected, args=None, kwargs=None)
st.sidebar.button('Fake Accident', help="Simulate accident situation",
                  on_click=accident_occured, args=None, kwargs=None)


st.subheader("Simulation Environment")
connectivity = st.checkbox('Network Connectivity')
if connectivity:
    st.session_state.connectivity = True
    st.success('Direct network connection available')
else:
    st.session_state.connectivity = False
    st.error("Network Down")

st.subheader("Vehicle Parameters")
columns = st.columns(3)
with columns[0]:
    st.metric(label="Temperature",
              value=f"{random.randrange(18,25):4.1f} °C", delta=f"{random.random():3.1f} °C")
with columns[1]:
    st.metric(label="Humidity",
              value=f"{random.randrange(35,42):4.1f} %", delta=f"{random.random():3.1f} ")
with columns[2]:
    st.metric(label="Fuel Level",
              value=f"{random.randrange(90,95):4.1f} %", delta=f"{random.random():3.1f} °C")

st.session_state.lat = 12.3368395802583 + random.random() - 1
st.session_state.lon = 76.67860115950155 + random.random()
df = pd.DataFrame(
    [[st.session_state.lat, st.session_state.lon]],
    columns=['lat', 'lon'])
st.map(df)
information_container = st.empty()
