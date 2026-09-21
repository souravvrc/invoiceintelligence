import joblib
import pandas as pd
from pathlib import Path

import streamlit as st

@st.cache_resource
def load_model():
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler

# Correct model paths
MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "invoice_flagging"
    / "models"
    / "predict_flag_invoice.pkl"
)

SCALER_PATH = (
    Path(__file__).resolve().parent.parent
    / "invoice_flagging"
    / "models"
    / "scaler.pkl"
)


def load_model():
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler


def predict_invoice_flag(input_data):

    model, scaler = load_model()

    df = pd.DataFrame(input_data)

    df_scaled = scaler.transform(df)

    prediction = model.predict(df_scaled)
    probability = model.predict_proba(df_scaled)

    df["Predicted_Flag"] = prediction
    df["Confidence"] = probability.max(axis=1)

    return df