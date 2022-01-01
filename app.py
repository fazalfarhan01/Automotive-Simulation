from numpy import byte
import streamlit as st
import random
from time import sleep
import pandas as pd
import json
import rsa
import requests
import base64
import requests

from port_scanner import get_near_by_nodes


publicKey, privateKey = rsa.newkeys(1024)


def show_information():
    data = {
        'device_id': 'id_001',
        'location': {
            'latitude': st.session_state.lat,
            'longitude': st.session_state.lon,
        }
    }

    st.info("Sending information to emergency services.")

    # id direct connection is available
    if st.session_state.connectivity:
        with st.spinner('Requesting server public key'):
            serverPublicKey = response = requests.get(
                "http://localhost:8500/keys").content.decode()

        encrypted = rsa.encrypt(json.dumps(data).encode(
        ), rsa.PublicKey(int(serverPublicKey), 65537))

        b64_encStr = base64.b64encode(encrypted)
        to_send = b64_encStr.decode("utf-8")
        with st.spinner('Sending Information...!'):
            response = requests.post(
                url=f'http://localhost:8500/receive/',
                json={'encrypted': to_send}
            )
            status = json.loads(response.content)['status']
        if status:
            st.success(
                'Information sent. Emergency services must be on their way.')
        else:
            st.error('Server failed to decrypt info.')
    # if direct connection is not available
    else:
        st.warning("Couldn't connect to server.")
        with st.spinner('Initiating peer2peer mode.'):
            near_by_node = get_near_by_nodes()
            sleep(2)
        st.success(f"Connected to nearby node: {near_by_node}")
        with st.spinner('Requesting server public key'):
            serverPublicKey = requests.get(
                url=f'http://{near_by_node}:8502/getKeys/').content.decode()
        encrypted = rsa.encrypt(json.dumps(data).encode(
        ), rsa.PublicKey(int(serverPublicKey), 65537))

        b64_encStr = base64.b64encode(encrypted)
        to_send = b64_encStr.decode("utf-8")

        with st.spinner('Sending info..!'):
            response = requests.post(
                url=f'http://{near_by_node}:8502/forward/',
                json={'encrypted': to_send}
            )
            status = json.loads(response.content)['status']
        if status:
            st.success(
                'Information sent. Emergency services must be on their way.')
        else:
            st.error('Failed to send information. Node has discarded your.')
    st.json(data)
    sleep(10)


def panic_triggered():
    with status_container.container():
        st.warning("Panic button pressed.")
        show_information()


def alcohol_detected():
    with status_container.container():
        st.error('Alcohol button clicked')
        show_information()


def accident_occured():
    with status_container.container():
        st.error('Accident button clicked')
        show_information()


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
