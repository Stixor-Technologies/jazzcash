from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from data_preprocessor import preprocess_test

# Define input data model using Pydantic
from pydantic import BaseModel, Field
from typing import Optional
from Rules import BusinessRules, StatisticalRules


# Initialize FastAPI app
app = FastAPI()

# Load model, scaler, and encoder
model = joblib.load('lgbm_classifier.pkl')
scaler = joblib.load('lgbm_scaler.pkl')
encoder = joblib.load('lgbm_encoder.pkl')


# Feature configuration for reference

# features = {
#     'continous': ['Amount', 'Old_Balance', 'New_Balance', 'Service_Charges'],
#     'drop': ['Transaction_Id', 'Date_Time', 'Phone_Number', 'CNIC', 'Name', 'Remarks'],
#     'categorical': [
#         'Type', 'ID_Source', 'Source_State', 'Source_City',
#         'Device_Name', 'IMEI', 'KYC_Status', 'Channel',
#         'ID_Dest', 'Dest_State', 'Dest_City'
#     ]
# }

class TransactionInput(BaseModel):
    Transaction_Id: Optional[str] = Field(alias="Transaction_Id")
    Date_Time: Optional[str] = Field(alias="Date_Time")
    Account_Creation_Date: Optional[str] = Field(alias="Account_Creation_Date")
    Phone_Number: Optional[str] = Field(alias="Phone_Number")
    CNIC: Optional[str]
    Name: Optional[str]
    Type: str
    Amount: float
    ID_Source: str = Field(alias="ID_Source")
    Old_Balance: float = Field(alias="Old_Balance")
    New_Balance: float = Field(alias="New_Balance")
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

@app.get("/")
def read_root():
    return {"message": "LightGBM ML API with preprocessing is running!"}

@app.post("/predict")
def predict(transaction: dict):
    try:
        # Convert input to DataFrame
        df = pd.DataFrame([transaction])

        # Preprocess the data
        processed_data = preprocess_test(df,scaler,encoder)

        transaction_id = df['Transaction_Id'][0]

        business = BusinessRules(df)
        statistical = StatisticalRules(df)

        business_results = business.apply_rules(transaction_id)

        statistical_results = statistical.apply_rules(transaction_id)

        prediction = model.predict(processed_data)

        return {"prediction Model LGBM": prediction.tolist(),
                "Prediction Business Rules" : business_results,
                "Prediction Statiscal Rules" : statistical_results} 

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
