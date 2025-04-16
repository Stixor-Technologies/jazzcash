import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OrdinalEncoder




def preprocess(df):
    """
    Preprocesses the input DataFrame by extracting datetime features, 
    normalizing continuous features, and encoding categorical features.

    Args:
        df (pd.DataFrame): Input DataFrame containing at least the following columns:
            - 'Date_Time' (datetime string): Timestamp of the transaction.
            - 'Account_Creation_Date' (datetime string): Account creation timestamp.
            - 'Amount', 'Old_Balance', 'New_Balance', 'Service_Charges' (float): Continuous features.
            - Various object-type columns (e.g., 'Transaction_Type', 'Location') for encoding.
            - Columns to be dropped: 'Transaction_Id', 'Date_Time', 'Phone_Number', 'CNIC', 'Name', 
              'Remarks', 'IMEI', 'Account_Creation_Date'.

    Returns:
        tuple: A tuple containing:
            - df_normalized (pd.DataFrame): Preprocessed DataFrame with datetime features, 
              normalized continuous features, and encoded categorical features.
            - scaler (MinMaxScaler): Scaler used for normalizing continuous features.
            - encoder (OrdinalEncoder): Encoder used for categorical columns.
    """
    
    df['Date_Time'] = pd.to_datetime(df['Date_Time'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

    df['Year_DT'] = df['Date_Time'].dt.year
    df['Month_DT'] = df['Date_Time'].dt.month
    df['Day_DT'] = df['Date_Time'].dt.day
    df['Hour_DT'] = df['Date_Time'].dt.hour
    #df['Minute_DT'] = df['Date_Time'].dt.minute
    #df['Second_DT'] = df['Date_Time'].dt.second
    df['Weekday_DT'] = df['Date_Time'].dt.weekday
    df['Day_of_year_DT'] = df['Date_Time'].dt.dayofyear

    df['Account_Creation_Date'] = pd.to_datetime(df['Account_Creation_Date'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

    df['Year_Acr_DT'] = df['Account_Creation_Date'].dt.year
    df['Month_Acr_DT'] = df['Account_Creation_Date'].dt.month
    df['Day_Acr_DT'] = df['Account_Creation_Date'].dt.day
    df['Hour_Acr_DT'] = df['Account_Creation_Date'].dt.hour
    #df['Minute_Acr_DT'] = df['Account_Creation_Date'].dt.minute
    #df['Second_Acr_DT'] = df['Account_Creation_Date'].dt.second
    df['Weekday_Acr_DT'] = df['Account_Creation_Date'].dt.weekday
    df['Day_of_year_Acr_DT'] = df['Account_Creation_Date'].dt.dayofyear

    df = df.drop(['Transaction_Id', 'Date_Time', 'Phone_Number', 'CNIC', 'Name', 'Remarks','IMEI','Account_Creation_Date'],axis = 1)

    objs = []
    for col in df.columns:
        if df[col].dtype == 'O':
            objs.append(col)

    cont_features = ['Amount', 'Old_Balance', 'New_Balance','Service_Charges']
    
    df_normalized = df.copy()

    # scaling the numerical entries
    scaler = MinMaxScaler()
    df_normalized[cont_features] = scaler.fit_transform(df[cont_features])
    

    encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)

    le_data = pd.DataFrame(
    encoder.fit_transform(df[objs]),
    columns=objs,
    index=df.index  # keep original index
    )

    df_normalized[objs] = le_data

    # encoders = {}
    # le_data=df_normalized.copy()

    # for col in objs:
    #     le = LabelEncoder()
    #     le_data[col] = le.fit_transform(le_data[col])
    #     encoders[col] = le 

    return df_normalized, scaler, encoder

def preprocess_test(df, scaler, encoder):
    
    """
    Preprocesses a test DataFrame using a pre-fitted scaler and encoder.
    This ensures consistency with training data transformations.

    Args:
        df (pd.DataFrame): Input test DataFrame containing at least the following columns:
            - 'Date_Time' (datetime string): Timestamp of the transaction.
            - 'Account_Creation_Date' (datetime string): Account creation timestamp.
            - 'Amount', 'Old_Balance', 'New_Balance', 'Service_Charges' (float): Continuous features.
            - Various object-type columns (e.g., 'Transaction_Type', 'Location') for encoding.
            - Columns to be dropped: 'Transaction_Id', 'Date_Time', 'Phone_Number', 'CNIC', 'Name', 
              'Remarks', 'IMEI', 'Account_Creation_Date'.

        scaler (MinMaxScaler): Scaler object fitted on training data used to normalize continuous features.
        encoder (OrdinalEncoder): Encoder object fitted on training data used to transform categorical features.

    Returns:
        pd.DataFrame: Preprocessed test DataFrame with extracted datetime features, 
                      scaled numerical features, and encoded categorical features.
    """


    df['Date_Time'] = pd.to_datetime(df['Date_Time'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

    df['Year_DT'] = df['Date_Time'].dt.year
    df['Month_DT'] = df['Date_Time'].dt.month
    df['Day_DT'] = df['Date_Time'].dt.day
    df['Hour_DT'] = df['Date_Time'].dt.hour
    #df['Minute_DT'] = df['Date_Time'].dt.minute
    #df['Second_DT'] = df['Date_Time'].dt.second
    df['Weekday_DT'] = df['Date_Time'].dt.weekday
    df['Day_of_year_DT'] = df['Date_Time'].dt.dayofyear

    df['Account_Creation_Date'] = pd.to_datetime(df['Account_Creation_Date'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

    df['Year_Acr_DT'] = df['Account_Creation_Date'].dt.year
    df['Month_Acr_DT'] = df['Account_Creation_Date'].dt.month
    df['Day_Acr_DT'] = df['Account_Creation_Date'].dt.day
    df['Hour_Acr_DT'] = df['Account_Creation_Date'].dt.hour
    #df['Minute_Acr_DT'] = df['Account_Creation_Date'].dt.minute
    #df['Second_Acr_DT'] = df['Account_Creation_Date'].dt.second
    df['Weekday_Acr_DT'] = df['Account_Creation_Date'].dt.weekday
    df['Day_of_year_Acr_DT'] = df['Account_Creation_Date'].dt.dayofyear


    df = df.drop(['Transaction_Id', 'Date_Time', 'Phone_Number', 'CNIC', 'Name', 'Remarks','IMEI','Account_Creation_Date'],axis = 1)

    objs = [col for col in df.columns if df[col].dtype == 'O']
    
    cont_features = ['Amount', 'Old_Balance', 'New_Balance','Service_Charges']

    
    df[cont_features] = scaler.transform(df[cont_features])

    le_test = pd.DataFrame(
    encoder.transform(df[objs]),  # Note: use transform, NOT fit_transform
    columns=objs,
    index=df.index
    )

    df[objs] = le_test

    return df




#import pandas as pd
# from sklearn.preprocessing import MinMaxScaler, LabelEncoder

# def preprocess(df):

#     df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-', '_')

#     # Ensure datetime conversion
#     df['date_time'] = pd.to_datetime(df['date_time'])

#     # Extract datetime features
#     df['year'] = df['date_time'].dt.year
#     df['month'] = df['date_time'].dt.month
#     df['day'] = df['date_time'].dt.day
#     df['hour'] = df['date_time'].dt.hour
#     df['minute'] = df['date_time'].dt.minute
#     df['second'] = df['date_time'].dt.second
#     df['weekday'] = df['date_time'].dt.weekday
#     df['day_of_year'] = df['date_time'].dt.dayofyear

#     # Drop unnecessary columns
#     df = df.drop([
#         'transaction_id', 'date_time', 'phone_number', 'cnic', 'name', 'remarks'
#     ], axis=1)

#     # Identify categorical (object) columns
#     objs = [
#     'type', 'id_source', 'source_state', 'source_city',
#     'device_name', 'imei', 'kyc_status', 'channel',
#     'id_dest', 'dest_state', 'dest_city'
# ]

#     # Define continuous features
#     cont_features = ['amount', 'old_balance', 'new_balance', 'service_charges']
 
#     # Scale numeric columns
#     df_normalized = df.copy()
#     scaler = MinMaxScaler()
#     df_normalized[cont_features] = scaler.fit_transform(df[cont_features])

#     # Label encode categorical columns
#     encoders = {}
#     le_data = df_normalized.copy()

#     for col in objs:
#         le = LabelEncoder()
#         le_data[col] = le.fit_transform(le_data[col])
#         encoders[col] = le

#     return le_data, scaler, encoders

    