from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import pandas as pd
from datetime import datetime
from collections import deque
from geopy.distance import geodesic
import numpy as np

# Initialize FastAPI app
app = FastAPI()

# Load model, scaler, and encoder
model = joblib.load('/home/nazar/Muhammad Raees Azam/JazzCash_Raees/Code/jazzcash/models/lgbm_classifier.pkl')
scaler = joblib.load('/home/nazar/Muhammad Raees Azam/JazzCash_Raees/Code/jazzcash/models/lgbm_scaler.pkl')
encoder = joblib.load('/home/nazar/Muhammad Raees Azam/JazzCash_Raees/Code/jazzcash/models/lgbm_encoder.pkl')

# Business rules configuration
high_risk_cities = [101, 202]  # Example high-risk cities
high_risk_states = [10, 12]  # Example high-risk states
new_account_threshold = 10000  # Account ID threshold for newly created accounts
amount_threshold = 100000  # Transaction amount threshold
n, m = 3, 5  # Rule 1: 3 transactions in 5 minutes

# Define input data model using Pydantic
class TransactionInput(BaseModel):
    Transaction_Id: Optional[str] = Field(alias="Transaction_Id")
    Date_Time: Optional[str] = Field(alias="Date_Time")
    Phone_Number: Optional[str] = Field(alias="Phone_Number")
    CNIC: Optional[str]
    Name: Optional[str]
    Type: str
    Amount: float
    ID_Source: str = Field(alias="ID_Source")
    Old_Balance: float = Field(alias="Old_Balance")
    New_Balance: float = Field(alias="New_Bance")
    Source_State: str = Field(alias="Source_State")
    Source_City: str = Field(alias="Source_City")
    Device_Name: str = Field(alias="Device_Name")
    IMEI: str
    KYC_Status: str = Field(alias="KYC_Status")
    Service_Charges: float = Field(alias="Service_Charges")
    Channel: str
    Remarks: Optional[str]
    ID_Dest: str = Field(alias="ID_Dest")
    Dest_State: str = Field(alias="Dest_State")
    Dest_City: str = Field(alias="Dest_City")

    model_config = {
        "validate_by_name": True,
        "populate_by_name": True,
    }

# Define the statistical rules logic
def apply_statistical_rules(df: pd.DataFrame) -> pd.DataFrame:
    # Rule 5: Amount > mean + 3 * std for the user
    user_stats = df.groupby('ID_Source')['Amount'].agg(['mean', 'std']).reset_index()
    df = df.merge(user_stats, on='ID_Source', how='left')
    df['flag_high_amount'] = df['Amount'] > (df['mean'] + 3 * df['std'])

    # Rule 6: Time outside user's 99% activity window
    quantiles = df.groupby('ID_Source')['hour'].quantile([0.005, 0.995]).unstack()
    quantiles.columns = ['lower_bound', 'upper_bound']
    df = df.merge(quantiles, left_on='ID_Source', right_index=True)
    df['flag_time_outlier'] = ~df['hour'].between(df['lower_bound'], df['upper_bound'])

    # Rule 7: Flag Based on Sudden Distant Activity (using simulated city coordinates)
    city_coords = {
        'Lahore': (31.5497, 74.3436),
        'Karachi': (24.8607, 67.0011),
        'Islamabad': (33.6844, 73.0479),
        'Peshawar': (34.0151, 71.5249),
        'Quetta': (30.1798, 66.9750),
        'Multan': (30.1575, 71.5249),
        'Faisalabad': (31.4504, 73.1350),
        'Rawalpindi': (33.5651, 73.0169),
        'Hyderabad': (25.3960, 68.3578),
        'Sukkur': (27.7052, 68.8574),
    }

    df['timestamp'] = pd.to_datetime(df['Date_Time'])
    df.sort_values(by=['ID_Source', 'timestamp'], inplace=True)
    df['flag_distance_time'] = False
    DIST_THRESHOLD = 200  # in kilometers
    TIME_THRESHOLD = 10   # in minutes

    # Loop over transactions grouped by user
    for user_id, group in df.groupby('ID_Source'):
        group = group.reset_index()
        for i in range(1, len(group)):
            prev_city = group.loc[i - 1, 'Source_City']
            curr_city = group.loc[i, 'Source_City']
            prev_time = group.loc[i - 1, 'timestamp']
            curr_time = group.loc[i, 'timestamp']

            # Get coordinates
            prev_coords = city_coords.get(prev_city)
            curr_coords = city_coords.get(curr_city)

            # Proceed if both cities have coordinates
            if prev_coords and curr_coords:
                distance = geodesic(prev_coords, curr_coords).kilometers
                time_diff = (curr_time - prev_time).total_seconds() / 60.0  # in minutes

                if distance > DIST_THRESHOLD and time_diff < TIME_THRESHOLD:
                    df.at[group.loc[i, 'index'], 'flag_distance_time'] = True

    # Rule 8: Flag transaction if the transaction count in current session is greater than median user transaction count per session
    df['prev_time'] = df.groupby('ID_Source')['timestamp'].shift()
    df['time_diff'] = (df['timestamp'] - df['prev_time']).dt.total_seconds() / 60.0
    df['new_session'] = (df['time_diff'] > 15) | (df['time_diff'].isna())
    df['session_id'] = df.groupby('ID_Source')['new_session'].cumsum()

    session_counts = df.groupby(['ID_Source', 'session_id']).size().reset_index(name='session_txn_count')
    median_txn_per_session = session_counts.groupby('ID_Source')['session_txn_count'].median().reset_index(name='median_count')

    df = df.merge(session_counts, on=['ID_Source', 'session_id'])
    df = df.merge(median_txn_per_session, on='ID_Source')
    df['flag_heavy_session'] = df['session_txn_count'] > df['median_count']

    return df

# Business rule checks
def apply_business_rules(df: pd.DataFrame) -> pd.DataFrame:
    # Apply statistical rules
    df = apply_statistical_rules(df)

    # Rule 1: Flag n transactions within m minutes
    df['timestamp'] = pd.to_datetime(df['Date_Time'])
    df['flag_rapid_txns'] = 0  # Initialize flag column
    for _, group in df.groupby('ID_Source'):
        dq = deque()
        for i, t in enumerate(group['timestamp']):
            dq.append(t)
            while (dq[-1] - dq[0]).total_seconds() > m * 60:
                dq.popleft()
            if len(dq) >= n:
                df.loc[group.index[i], 'flag_rapid_txns'] = 1

    # Rule 2: Flag transactions from/to high-risk cities
    df['flag_high_risk_city'] = df['Source_City'].isin(high_risk_cities) | df['Dest_City'].isin(high_risk_cities)

    # Rule 3: Flag transactions from high-risk region and odd time (e.g., 12 AM - 5 AM)
    df['hour'] = df['timestamp'].dt.hour
    df['flag_risky_time_region'] = ((df['Source_State'].isin(high_risk_states)) & (df['hour'].between(0, 5)))

    # Rule 4: Flag newly created receiving account and large amount
    df['flag_new_acc_large_amt'] = ((df['ID_Dest'].astype(int) > new_account_threshold) & (df['Amount'] > amount_threshold))

    return df

@app.get("/")
def read_root():
    return {"message": "LightGBM ML API with business rules and preprocessing is running!"}

@app.post("/predict")
def predict(transaction: TransactionInput):
    try:
        # Convert input to DataFrame
        input_dict = transaction.dict()
        df = pd.DataFrame([input_dict])

        # Apply business rules
        df = apply_business_rules(df)

        # Preprocess the data
        processed_data = preprocess_test(df, scaler, encoder)

        # Make prediction
        prediction = model.predict(processed_data)

        # Return business rule flags along with the prediction
        response = {
            "prediction": prediction.tolist(),
            "business_rules_flags": {
                "flag_rapid_txns": df['flag_rapid_txns'].iloc[0],
                "flag_high_risk_city": df['flag_high_risk_city'].iloc[0],
                "flag_risky_time_region": df['flag_risky_time_region'].iloc[0],
                "flag_new_acc_large_amt": df['flag_new_acc_large_amt'].iloc[0],
                "flag_high_amount": df['flag_high_amount'].iloc[0],
                "flag_time_outlier": df['flag_time_outlier'].iloc[0],
                "flag_distance_time": df['flag_distance_time'].iloc[0],
                "flag_heavy_session": df['flag_heavy_session'].iloc[0]
            }
        }
        return response

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
