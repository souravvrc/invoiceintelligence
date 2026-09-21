import streamlit as st
import pandas as pd
import numpy as np
from inference.predict_freight import predict_freight_cost
from inference.predict_invoice_flag import predict_invoice_flag

# Page Configuration
st.set_page_config(
    page_title="Vendor Invoice Intelligence Portal",
    page_icon="🚚",
    layout="wide",
)
# Header Section
st.markdown(
    """
# 🚚 Vendor Invoice Intelligence Portal
### AI-DRiven Freight Cost Prediction & Invoice Risk Flagging

This internal analytics portal leverages machine learning to
- **Forecast freight cost accurately**
- **Detect risky or abnormal vendor invoices**
- **Reduce financial leakage and manual workload**
    """
)

st.divider()

# Slider

st.sidebar.title(" Model Selection")
selected_model = st.sidebar.radio(
    "Choose Prediction Module",
    [
        "Freight Cost Prediction",
        "Invoice Manual Approval Flag"
    ]
)

st.sidebar.markdown("""
---
**Business Impact:**
- Improved cost frecasting
- Reduced invoice fraud and anomalies
- Faster finance operations
"""
)

# Freight cost prediction
if selected_model == "Freight Cost Prediction":
    st.subheader("🚚 Freight Cost Prediction")
    st.markdown(
        """
        **Objective:** 
        Predict freight cost for a vendor invoice using **Invoice Dollars**
        to support budgeting, forecasting, and vendor negotiations.
        """
    )
    with st.form("freight_form"):
        dollars = st.number_input(
        "Invoice Dollars",
        min_value=1.0,
        value=18500.0
                )
        submit_freight = st.form_submit_button("Predict Freight Cost")

    if submit_freight:
         input_data = {
              "Dollars": [dollars]
         }

         prediction = predict_freight_cost(input_data)['Predicted_Freight']
         st.success("Prediction completed successfully!")

         st.metric(
              label = "Estimated Freight Cost",
              value = f"${prediction[0]:,.2f}"
         )
# Invoice flag prediction
else:
    st.subheader("⚠️ Invoice Manual Approval Flag Prediction")
    st.markdown(
        """
        **Objective:** 
        Predict whether a vendor invoice requires manual approval based on **Quantity** and **Invoice Dollars** to identify potential risks and anomalies.
        """
    )
    with st.form("invoice_form"):
        col1,col2,col3 = st.columns(3)
        with col1:
            invoice_quantity = st.number_input("Invoice Quantity", min_value=1, value = 50)
            freight = st.number_input(
                "Freight Cost ($)",
                min_value=0.0,
                value = 1.73
            )
        with col2:
                invoice_dollars = st.number_input(
                     "Invoice Dollars",
                     min_value=1.0,
                     value = 352.95
                )
                total_item_quantity = st.number_input(
                        "Total Item Quantity",
                        min_value=1,
                        value = 162
                )
        with col3:
                total_item_dollars = st.number_input(
                        "Total Item Dollars",
                        min_value=1.0,
                        value = 2476.0
                )
        submit_flag = st.form_submit_button("Evaluate Invoice Risk")
    
    if submit_flag:
         input_data = {
                "invoice_quantity": [invoice_quantity],
                "invoice_dollars": [invoice_dollars],
                "Freight": [freight],
                "total_item_quantity": [total_item_quantity],
                "total_item_dollars": [total_item_dollars]
         }
         result = predict_invoice_flag(input_data)
         
         is_flagged = bool(result['Predicted_Flag'][0])
         confidence = result['Confidence'][0]
         
         if is_flagged:
              st.error("⚠️ This invoice requires **Manual Approval**")
              st.metric(
                   "Model Confidence",
                   f"{confidence*100:.1f}%"
                   )
         else:
              st.success("✅ This invoice is **Safe for Auto-Approval**")
              st.metric(
                   "Model Confidence",
                   f"{confidence*100:.1f}%"
                   )
         