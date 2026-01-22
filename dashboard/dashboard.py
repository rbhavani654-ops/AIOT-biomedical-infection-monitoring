import streamlit as st
import pandas as pd
import os

DATA_FILE = "../backend/data/sample_data.csv"

st.title("AIoT Biomedical Infection Monitoring Dashboard")

if not os.path.exists(DATA_FILE):
  st.warning("No data file yet. Start server and ESP32 first.")
  st.stop()

@st.cache_data
def load_data():
  df = pd.read_csv(DATA_FILE)
  df["timestamp"] = pd.to_datetime(df["timestamp"])
  return df

df = load_data()

if df.empty:
  st.warning("Data file is empty. Wait for ESP32 to send some data.")
  st.stop()

patient_ids = df["patient_id"].unique().tolist()
selected_patient = st.selectbox("Select Patient", patient_ids)

pdf = df[df["patient_id"] == selected_patient].sort_values("timestamp")

st.line_chart(
  pdf.set_index("timestamp")[["temperature", "heart_rate", "spo2"]],
)

st.subheader("Latest Readings")
st.write(pdf.tail(5))
