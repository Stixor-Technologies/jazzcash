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

# Get weightages from user and ensure they do not exceed 100
while True:
    try:
        business_weight = float(input("Enter weightage for Business Rules (0-100): "))
        statistical_weight = float(input("Enter weightage for Statistical Rules (0-100): "))
        if business_weight < 0 or business_weight > 100 or statistical_weight < 0 or statistical_weight > 100:
             print("❌ Error: Weights must be between 0 and 100.")
             print("Please enter valid weightages again.\n")
             continue

        total = business_weight + statistical_weight
        
        if total > 100:
            print("❌ Error: The combined weight of Business and Statistical Rules exceeds 100.")
            print("Please enter valid weightages again.\n")
        else:
            model_weight = 100 - total
            break
    except ValueError:
        print("❌ Invalid input. Please enter numeric values only.\n")

# Show final weights
print(f"\n✅ Weight Distribution:")
print(f"Business Rules Weightage: {business_weight}%")
print(f"Statistical Rules Weightage: {statistical_weight}%")
print(f"Model (Auto-assigned) Weightage: {model_weight}%")

# Business Rules check
business = BusinessRules(df)
business_results, business_score = business.apply_rules(transaction_id)
business_percentage = (business_score / 100) * 100

print("\nBusiness Rules Results:")
for rule, result in business_results.items():
    print(f"{rule}: {'Flagged' if result else 'Not Flagged'}")
print(f"Business Rules Score: {business_score}/100")
print(f"Business Rules Score Percentage: {business_percentage:.2f}%")

# Statistical Rules check
statistical = StatisticalRules(df)
statistical_results, statistical_score = statistical.apply_rules(transaction_id)
statistical_percentage = (statistical_score / 100) * 100

print("\nStatistical Rules Results:")
for rule, result in statistical_results.items():
    print(f"{rule}: {'Flagged' if result else 'Not Flagged'}")
print(f"Statistical Rules Score: {statistical_score}/100")
print(f"Statistical Rules Score Percentage: {statistical_percentage:.2f}%")

# Model score (hardcoded)
model_score = 98
model_percentage = model_score

print(f"\nModel Score: {model_score}/100")

# Final weighted score calculation
final_score = (
    (business_percentage * business_weight / 100) +
    (statistical_percentage * statistical_weight / 100) +
    (model_percentage * model_weight / 100)
)

print(f"\n🧮 Final Weighted Risk Score: {final_score:.2f}/100")

# Risk classification
if final_score >= 75:
    print("⚠️ High Risk Transaction")
elif final_score >= 50:
    print("⚠️ Medium Risk Transaction")
else:
    print("✅ Low Risk Transaction")
