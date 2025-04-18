from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from python_files.data_preprocessor import preprocess_test
import numpy as np

# Define input data model using Pydantic
from pydantic import BaseModel, Field
from typing import Optional
from python_files.Rules import BusinessRules, StatisticalRules


# Initialize FastAPI app
app = FastAPI()

# Load model, scaler, and encoder
model = joblib.load('models\lgbm_classifier.pkl')
scaler = joblib.load('models\lgbm_scaler.pkl')
encoder = joblib.load('models\lgbm_encoder.pkl')
encoder_dict = joblib.load("models\encoder_dict.pkl")


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

@app.get("/weights")
def get_weights():
    try:
        # Return the default weights
        weights = {
            "business_weight": 20,
            "statistical_weight": 30,
            "model_weight": 50
        }
        return weights
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/predict")
def predict(transaction: dict):
    try:

        business_weight = transaction.pop('business_weight')  # Default to 20 if not provided
        statistical_weight = transaction.pop('statistical_weight')  # Default to 30 if not provided
        model_weight = transaction.pop('model_weight')

        # Convert input to DataFrame
        df = pd.DataFrame([transaction])

        # Preprocess the data
        processed_data = preprocess_test(df,scaler,encoder_dict)

        transaction_id = df['Transaction_Id'][0]

        business = BusinessRules(df)
        statistical = StatisticalRules(df)

        business_results, business_score = business.apply_rules(transaction_id)
        business_percentage = business_score * business_weight / 100
        

        statistical_results, statistical_score = statistical.apply_rules(transaction_id)
        statistical_percentage = statistical_score * statistical_weight / 100
        

        prob_model = model.predict_proba(processed_data)

        # Convert probabilities to binary class labels based on the threshold
        prediction_model = model.predict(processed_data)

        if prediction_model == 1:
            model_percentage = np.round(float(np.max(prob_model)) * 100, 2)
        else:
            model_percentage = np.round(100 - (float(np.max(prob_model)) * 100), 2)

        final_score = (
        (business_percentage) +
        (statistical_percentage) +
        (model_percentage * model_weight / 100)
        )

        threshold = 50

        if final_score > threshold:
            prediction = 1
        else:
            prediction = 0

        return {"Accumulative Prediction" : np.round(final_score,2),
                "Prediction Model LGBM": prediction,
                "Probability Model" : model_percentage.tolist(),
                "Prediction Business Rules" : business_results,
                "Probability Business Rules" : business_percentage,
                "Prediction Statiscal Rules" : statistical_results,
                "Probability Statistical Rules" : statistical_percentage} 

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/explain-prediction")
def explain_prediction():
    try:
        # Instantiate dummy DataFrame for rule fetching
        dummy_df = pd.DataFrame([{}])
        business = BusinessRules(dummy_df)
        statistical = StatisticalRules(dummy_df)

        business_rule_list = business.list_rules()
        statistical_rule_list = statistical.list_rules()

        return {
            "Business Rules": business_rule_list,
            "Statistical Rules": statistical_rule_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
