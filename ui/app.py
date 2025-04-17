import streamlit as st
import requests
import datetime

st.title("Fraud Predictor (LightGBM)")
st.write("Enter transaction details to get a fraud prediction.")

current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Retrieve the weights from the API
weights_response = requests.get("http://127.0.0.1:8000/weights")
if weights_response.status_code == 200:
    weights = weights_response.json()
else:
    st.error(f"Error: {weights_response.json().get('detail', 'Unknown error')}")
    weights = {"business_weight": 20, "statistical_weight": 30, "model_weight": 50}

# Input fields for the transaction data

# test_case_1 = {
#     "Transaction_Id": st.text_input("Transaction ID", "262874940"),
#     "Account_Creation_Date": st.text_input("Date Account_Creation_Date", "2025-11-20 03:51:50"),
#     "Date_Time": st.text_input("Date Time", "2025-11-22 03:51:50"),
#     "Phone_Number": st.text_input("Phone Number", "+92 333 2569874"),
#     "CNIC": st.text_input("CNIC", "40734-8820668-3"),
#     "Name": st.text_input("Name", "Fariha Mirza"),
#     "Type": st.selectbox("Type", ["Utility Bill Payment", "PAYMENT", "TRANSFER", "WITHDRAWAL"]),
#     "Amount": st.number_input("Amount", value=1740100.97),
#     "ID_Source": st.text_input("ID Source", "C12345896"),
#     "Old_Balance": st.number_input("Old Balance", value=9987000.00),
#     "New_Balance": st.number_input("New Balance", value=0.00),
#     "Source_State": st.text_input("Source State", "Unknown"),
#     "Source_City": st.text_input("Source City", "Unknown"),
#     "Device_Name": st.text_input("Device Name", "Xiaomi Mi 11"),
#     "IMEI": st.text_input("IMEI", "601635731712294"),
#     "KYC_Status": st.selectbox("KYC Status", ["Verified", "On-Hold", "Not Verified"]),
#     "Service_Charges": st.number_input("Service Charges", value=34.80),
#     "Channel": st.text_input("Channel", "Mobile Payments"),
#     "Remarks": st.text_input("Remarks", "Utility bill payment"),
#     "ID_Dest": st.text_input("ID Dest", "M1855643329"),
#     "Dest_State": st.text_input("Dest State", "Balochistan"),
#     "Dest_City": st.text_input("Dest City", "Dera Bugti"),
# }

# test_case_2 = {
#     "Transaction_Id": st.text_input("Transaction ID", "263099341"),
#     "Account_Creation_Date": st.text_input("Date Account_Creation_Date", "2025-10-08"),
#     "Date_Time": st.text_input("Date Time", "2025-10-10 14:18:44"),
#     "Phone_Number": st.text_input("Phone Number", "Not Provided"),
#     "CNIC": st.text_input("CNIC", "42101-2290987-9"),
#     "Name": st.text_input("Name", "Salman Khalid"),
#     "Type": st.selectbox("Type", ["Wallet-to-Wallet Transfer", "PAYMENT", "TRANSFER", "WITHDRAWAL"]),
#     "Amount": st.number_input("Amount", value=2490000.00),
#     "ID_Source": st.text_input("ID Source", "C1789461102"),
#     "Old_Balance": st.number_input("Old Balance", value=2500000.00),
#     "New_Balance": st.number_input("New Balance", value=0.00),
#     "Device_Name": st.text_input("Device Name", "Infinix Zero X Neo"),
#     "IMEI": st.text_input("IMEI", "351760319091001"),
#     "KYC_Status": st.selectbox("KYC Status", ["Verified", "On-Hold", "Not Verified", "Pending"]),
#     "Service_Charges": st.number_input("Service Charges", value=50.00),
#     "Channel": st.text_input("Channel", "Mobile App"),
#     "Remarks": st.text_input("Remarks", "Wallet Transfer"),
#     "ID_Dest": st.text_input("ID Dest", "M1187643899"),
#     "Dest_State": st.text_input("Dest State", "Sindh"),
#     "Dest_City": st.text_input("Dest City", "Lyari Town"),
#     "Source_State": st.text_input("Source State", "Punjab"),
#     "Source_City": st.text_input("Source City", "Rawalpindi"),
# }

test_case_3 = {
    "Transaction_Id": st.text_input("Transaction ID", "263741220"),
    "Account_Creation_Date": st.text_input("Date Account_Creation_Date", "2025-09-10"),
    "Date_Time": st.text_input("Date Time", "2025-09-16 12:33:22"),
    "Phone_Number": st.text_input("Phone Number", "+92 301-4539011"),
    "CNIC": st.text_input("CNIC", "35201-4938273-5"),
    "Name": st.text_input("Name", "Hina Arshad"),
    "Type": st.selectbox("Type", ["Biometric Cash Withdrawal", "PAYMENT", "TRANSFER", "WITHDRAWAL"]),
    "Amount": st.number_input("Amount", value=970000.00),
    "ID_Source": st.text_input("ID Source", "C1778241900"),
    "Old_Balance": st.number_input("Old Balance", value=1000000.00),
    "New_Balance": st.number_input("New Balance", value=30000.00),
    "Device_Name": st.text_input("Device Name", "Biometric POS Terminal #44"),
    "IMEI": st.text_input("IMEI", "867530921110212"),
    "KYC_Status": st.selectbox("KYC Status", ["Verified", "On-Hold", "Not Verified"]),
    "Service_Charges": st.number_input("Service Charges", value=15.00),
    "Channel": st.text_input("Channel", "POS Biometric"),
    "Remarks": st.text_input("Remarks", "Cash withdrawal via thumb"),
    "ID_Dest": st.text_input("ID Dest", "Not Applicable"),
    "Dest_State": st.text_input("Dest State", "Punjab"),
    "Dest_City": st.text_input("Dest City", "Gujranwala"),
    "Source_State": st.text_input("Source State", "Punjab"),
    "Source_City": st.text_input("Source City", "Gujranwala"),
}

# test_case_4 = {
#     "Transaction_Id": st.text_input("Transaction ID", "264411783"),
#     "Account_Creation_Date": st.text_input("Date Account_Creation_Date", "2024-11-12"),
#     "Date_Time": st.text_input("Date Time", "2025-08-19 13:11:00"),
#     "Phone_Number": st.text_input("Phone Number", "+92 334-2239841"),
#     "CNIC": st.text_input("CNIC", "61101-1982719-6"),
#     "Name": st.text_input("Name", "Saima Qureshi"),
#     "Type": st.selectbox("Type", ["Wallet-to-Bank Transfer", "PAYMENT", "TRANSFER", "WITHDRAWAL"]),
#     "Amount": st.number_input("Amount", value=78500.00),
#     "ID_Source": st.text_input("ID Source", "C1571002221"),
#     "Old_Balance": st.number_input("Old Balance", value=156000.00),
#     "New_Balance": st.number_input("New Balance", value=77450.00),
#     "Device_Name": st.text_input("Device Name", "Vivo Y21"),
#     "IMEI": st.text_input("IMEI", "353362791102234"),
#     "KYC_Status": st.selectbox("KYC Status", ["Verified", "On-Hold", "Not Verified"]),
#     "Service_Charges": st.number_input("Service Charges", value=50.00),
#     "Channel": st.text_input("Channel", "Mobile App"),
#     "Remarks": st.text_input("Remarks", "Monthly savings transfer"),
#     "ID_Dest": st.text_input("ID Dest", "M1443099022"),
#     "Dest_State": st.text_input("Dest State", "Punjab"),
#     "Dest_City": st.text_input("Dest City", "Lahore"),
#     "Source_State": st.text_input("Source State", "Punjab"),
#     "Source_City": st.text_input("Source City", "Islamabad"),
# }

transaction_data = test_case_3

# Sliders to adjust the weights
business_weight = st.slider("Business Weight", min_value=0, max_value=100, value=weights["business_weight"], step=1)
statistical_weight = st.slider("Statistical Weight", min_value=0, max_value=100, value=weights["statistical_weight"], step=1)
model_weight = st.slider("Model Weight", min_value=0, max_value=100, value=weights["model_weight"], step=1)

# Ensure the weights sum to 100
if business_weight + statistical_weight + model_weight != 100:
    st.warning("The sum of all weights must be 100. The current weights don't add up to 100.")

# Function to make prediction with adjusted weights
if st.button("Predict"):
    with st.spinner("Sending data to model..."):
        try:
            # Include the adjusted weights in the prediction data
            transaction_data["business_weight"] = business_weight
            transaction_data["statistical_weight"] = statistical_weight
            transaction_data["model_weight"] = model_weight

            # Send the data to the prediction API
            response = requests.post("http://127.0.0.1:8000/predict", json=transaction_data)
            
            if response.status_code == 200:
                result = response.json()


                # Display Model Prediction
                prediction = result.get("Prediction Model LGBM")
                #st.success(f"Prediction: {'Fraud' if prediction == 1 else 'Not Fraud'}")

                if prediction == 1:
                    st.markdown("<h4 style='color:red;'>Prediction: Fraud</h4>", unsafe_allow_html=True)
                else:
                    st.markdown("<h4 style='color:green;'>Prediction: Not Fraud</h4>", unsafe_allow_html=True)

                
                # Accumulative Prediction Calculation
                final_score = result.get("Accumulative Prediction", 0.0)
                st.subheader(f"Accumulative Prediction: {final_score:.2f}%")



                # Display Model Probability
                probability = result.get("Probability Model")
                st.info(f"Model Confidence: {probability:.2f}%")

                # Display Business Rule Flags with Probability
                business_flags = result.get("Prediction Business Rules", {})
                business_prob = result.get("Probability Business Rules", 0.0)
                st.subheader(f"Business Rule Flags (Score: {business_prob:.2f}%)")
                for rule_name, rule_value in business_flags.items():
                    st.write(f"• {rule_name}: {'Triggered' if rule_value else 'Not Triggered'}")

                # Display Statistical Rule Flags with Probability
                statistical_flags = result.get("Prediction Statiscal Rules", {})
                statistical_prob = result.get("Probability Statistical Rules", 0.0)
                st.subheader(f"Statistical Rule Flags (Score: {statistical_prob:.2f}%)")
                for rule_name, rule_value in statistical_flags.items():
                    st.write(f"• {rule_name}: {'Triggered' if rule_value else 'Not Triggered'}")

            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
