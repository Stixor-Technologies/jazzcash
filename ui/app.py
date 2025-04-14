# streamlit_app.py

import streamlit as st
import requests
import datetime

st.title("Fraud Predictor (LightGBM)")
st.write("Enter transaction details to get a fraud prediction.")

current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Input fields
transaction_data = {
    "Transaction_Id": st.text_input("Transaction ID", "1234567890"),
    "Date_Time": st.text_input("Date Time", current_datetime),
    "Phone_Number": st.text_input("Phone Number", "+92 300-1234567"),
    "CNIC": st.text_input("CNIC", "12345-6789012-3"),
    "Name": st.text_input("Name", "Ali Khan"),
    "Type": st.selectbox("Type", ["PAYMENT", "TRANSFER", "WITHDRAWAL"]),
    "Amount": st.number_input("Amount", value=5000.0),
    "ID_Source": st.text_input("ID Source", "C123456"),
    "Old_Balance": st.number_input("Old Balance", value=10000.0),
    "New_Balance": st.number_input("New Balance", value=5000.0),
    "Source_State": st.text_input("Source State", "Punjab"),
    "Source_City": st.text_input("Source City", "Lahore"),
    "Device_Name": st.text_input("Device Name", "Samsung S21"),
    "IMEI": st.text_input("IMEI", "356938035643809"),
    "KYC_Status": st.selectbox("KYC Status", ["Verified", "On-Hold", "Not Verified"]),
    "Service_Charges": st.number_input("Service Charges", value=50.0),
    "Channel": st.text_input("Channel", "Mobile Payments"),
    "Remarks": st.text_input("Remarks", "Electricity Bill"),
    "ID_Dest": st.text_input("ID Dest", "M987654"),
    "Dest_State": st.text_input("Dest State", "Sindh"),
    "Dest_City": st.text_input("Dest City", "Karachi"),
}


# transaction_data = {
#     "Transaction_Id": st.text_input("Transaction ID", "5720078885"),
#     "Date_Time": st.text_input("Date Time", "2021-04-05 18:32:15"),
#     "Phone_Number": st.text_input("Phone Number", "+92 305-3516186"),
#     "CNIC": st.text_input("CNIC", "63643-6029379-9"),
#     "Name": st.text_input("Name", "Bilal Qureshi"),
#     "Type": st.selectbox("Type", ["PAYMENT", "TRANSFER", "WITHDRAWAL"], index=1),
#     "Amount": st.number_input("Amount", value=837192.23),
#     "ID_Source": st.text_input("ID Source", "C653262851"),
#     "Old_Balance": st.number_input("Old Balance", value=837192.23),
#     "New_Balance": st.number_input("New Balance", value=0.0),
#     "Source_State": st.text_input("Source State", "Azad Kashmir"),
#     "Source_City": st.text_input("Source City", "Rawalakot"),
#     "Device_Name": st.text_input("Device Name", "OnePlus 9"),
#     "IMEI": st.text_input("IMEI", "468898808901590"),
#     "KYC_Status": st.selectbox("KYC Status", ["Validated", "On-Hold", "Not Verified"], index=0),
#     "Service_Charges": st.number_input("Service Charges", value=1674.38446),
#     "Channel": st.text_input("Channel", "Bank Transfer"),
#     "Remarks": st.text_input("Remarks", ""),
#     "ID_Dest": st.text_input("ID Dest", "C690345380"),
#     "Dest_State": st.text_input("Dest State", "Gilgit-Baltistan"),
#     "Dest_City": st.text_input("Dest City", "Skardu"),
# }



# Prediction trigger
if st.button("Predict"):
    with st.spinner("Sending data to model..."):
        try:
            response = requests.post("http://127.0.0.1:8000/predict", json=transaction_data)
            if response.status_code == 200:

                result = response.json()

                prediction = result["prediction Model LGBM"][0]
                st.success(f"Prediction: {'Fraud' if prediction == 1 else 'Not Fraud'}")

                # Show business rule flags
                st.write("Business Rule Flags:")
                st.write(f"• New Account Large Amount: {result['New Account Large Amount'][0]}")
                st.write(f"• Risky Time Region: {result['Risky Time Region'][0]}")
                st.write(f"• High Risk City: {result['High Risk City'][0]}")
                st.write(f"• Rapid Transactions: {result['Rapid Transactions'][0]}")
            else:
                st.error(f"Error: {response.json()['detail']}")
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
