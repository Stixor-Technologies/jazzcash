import pandas as pd
from Rules import BusinessRules, StatisticalRules

# Sample transaction data
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

# Convert to DataFrame
df = pd.DataFrame([data])
df['Date_Time'] = pd.to_datetime(df['Date_Time'])

# Set Transaction ID
transaction_id = '262874940'

print("Transaction Data:")
print(df)

# Business Rules check
business = BusinessRules(df)
business_results, business_score = business.apply_rules(transaction_id)
print("\nBusiness Rules Results:")
print("\nbusiness_results:",business_results)
print("\nbusiness_score:",business_score)
for rule, result in business_results.items():
    print(f"{rule}: {'Flagged' if result else 'Not Flagged'}")
print(f"Business Rules Score: {business_score}/100")
print(f"Business Rules Score Percentage: {(business_score/100)*100}")

# Statistical Rules check
statistical = StatisticalRules(df)
statistical_results, statistical_score = statistical.apply_rules(transaction_id)
print("\nStatistical Rules Results:")
print("\nstatistical_results:",statistical_results)
print("\nstatistical_score:",statistical_score)
for rule, result in statistical_results.items():
    print(f"{rule}: {'Flagged' if result else 'Not Flagged'}")
print(f"Statistical Rules Score: {statistical_score}/100")
print(f"Statistical Rules Score Percentage: {(statistical_score/100)*100}")
