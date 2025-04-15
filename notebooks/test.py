import pandas as pd
from datetime import datetime

# Import the classes from Rules.py
from Rules import FraudRulesEngine

# Sample DataFrame initialization (test data)
# data = {
#     'Transaction_Id': ['262874940'],
#     'Date_Time': ['2025-11-22 03:51:50'],
#     'Account_Creation_Date': ['2025-11-20 07:51:50'],
#     'Phone_Number': ['+92 316-5932748'],
#     'CNIC': ['40734-8820668-3'],
#     'Name': ['Fariha Mirza'],
#     'Type': ['PAYMENT'],
#     'Amount': [1740100.97],
#     'ID_Source': ['C1715563227'],
#     'Old_Balance': [9987000.00],
#     'New_Balance': [0.00],
#     'Device_Name': ['Xiaomi Mi 11'],
#     'IMEI': ['601635731712294'],
#     'KYC_Status': ['On-Hold'],
#     'Service_Charges': [34.80394],
#     'Channel': ['Mobile Payments'],
#     'Remarks': ['Utility bill payment'],
#     'ID_Dest': ['M1855643329'],
#     'Dest_State': ['Balochistan'],
#     'Dest_City': ['Dera Bugti'],
#     'Source_City': ['Dera Bugti'],
#     'Is_Fraud': ['0'],
# }


data = {
    'Transaction_Id': '262874940',
    'Date_Time': '2025-11-22 03:51:50',
    'Account_Creation_Date': '2025-11-20 07:51:50',
    'Phone_Number': '+92 316-5932748',
    'CNIC': '40734-8820668-3',
    'Name': 'Fariha Mirza',
    'Type': 'PAYMENT',
    'Amount': 1740100.97,
    'ID_Source': 'C1715563227',
    'Old_Balance': 9987000.00,
    'New_Balance': 0.00,
    'Device_Name': 'Xiaomi Mi 11',
    'IMEI': '601635731712294',
    'KYC_Status': 'On-Hold',
    'Service_Charges': 34.80394,
    'Channel': 'Mobile Payments',
    'Remarks': 'Utility bill payment',
    'ID_Dest': 'M1855643329',
    'Dest_State': 'Balochistan',
    'Dest_City': 'Dera Bugti',
    'Source_City': 'Dera Bugti',
    'Is_Fraud': '0',
}


# Create DataFrame from the test data
df = pd.DataFrame([data])
# Convert 'Date_Time' to datetime
df['Date_Time'] = pd.to_datetime(df['Date_Time'])

# Initialize the FraudRulesEngine with the test DataFrame
engine = FraudRulesEngine(df)

# Specify the Transaction ID you want to test
transaction_id = '262874940'


result = engine.apply_all_rules(transaction_id=transaction_id)

if result:
    print(f"\nFlag Status for Transaction {transaction_id}:\n")

    for rule_name, flagged_ids in result['flagged_by_rule'].items():
        status = "TRUE" if transaction_id in flagged_ids else "FALSE"
        print(f"{rule_name}: {status}")

    print("\nCombined Flagged Transactions:")
    print(result['combined_flagged_transactions'])

else:
    print("Transaction not found or error occurred.")
