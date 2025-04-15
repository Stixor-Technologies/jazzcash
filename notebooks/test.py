# test.py

import pandas as pd
from datetime import datetime

# Import the classes from Rules.py
from Rules import FraudRulesEngine

# Sample DataFrame initialization (test data)
data = {
    'Transaction_Id': ['262874940'],
    'Date_Time': ['2025-11-22 03:51:50'],
    'Account_Creation_Date': ['2025-11-20 07:51:50'],
    'Phone_Number': ['+92 316-5932748'],
    'CNIC': ['40734-8820668-3'],
    'Name': ['Fariha Mirza'],
    'Type': ['PAYMENT'],
    'Amount': [1740100.97],
    'ID_Source': ['C1715563227'],
    'Old_Balance': [9987000.00],
    'New_Balance': [0.00],
    'Device_Name': ['Xiaomi Mi 11'],
    'IMEI': ['601635731712294'],
    'KYC_Status': ['On-Hold'],
    'Service_Charges': [34.80394],
    'Channel': ['Mobile Payments'],
    'Remarks': ['Utility bill payment'],
    'ID_Dest': ['M1855643329'],
    'Dest_State': ['Balochistan'],
    'Dest_City': ['Dera Bugti'],
    'Source_City': ['Dera Bugti'],
    'Is_Fraud': ['0'],
    
}

# Create DataFrame from the test data
df = pd.DataFrame(data)

# Initialize the FraudRulesEngine with the test DataFrame
engine = FraudRulesEngine(df)

# Apply all fraud detection rules
result = engine.apply_all_rules()

# Print the flagged transactions for each rule
print("Flagged Transactions by Rule:")
for rule, txns in result['flagged_by_rule'].items():
    print(f"{rule}: {len(txns)} flagged")

# Print the combined unique flagged transactions
print("\nTotal Unique Flagged Transactions:", len(result['combined_flagged_transactions']))

# Optionally, print all flagged transactions for inspection
print("\nCombined Flagged Transaction IDs:")
for txn_id in result['combined_flagged_transactions']:
    print(txn_id)
