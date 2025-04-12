import pandas as pd
from sklearn.preprocessing import MinMaxScaler , LabelEncoder


def preprocess(df):
    df['Date Time'] = pd.to_datetime(df['Date Time'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    df['year'] = df['Date Time'].dt.year
    df['month'] = df['Date Time'].dt.month
    df['day'] = df['Date Time'].dt.day
    df['hour'] = df['Date Time'].dt.hour
    df['minute'] = df['Date Time'].dt.minute
    df['second'] = df['Date Time'].dt.second
    df['weekday'] = df['Date Time'].dt.weekday
    df['day_of_year'] = df['Date Time'].dt.dayofyear

    df = df.drop(['Transaction Id', 'Date Time', 'Phone Number', 'CNIC', 'Name', 'Remarks'],axis = 1)

    objs = []
    for col in df.columns:
        if df[col].dtype == 'O':
            objs.append(col)

    cont_features = ['Amount', 'Old Balance', 'New Balance','Service Charges']
    
    df_normalized = df.copy()

    # scaling the numerical entries
    scaler = MinMaxScaler()
    df_normalized[cont_features] = scaler.fit_transform(df[cont_features])
    

    # label encoding the data 
    encoders = {}
    le_data=df_normalized.copy()

    for col in objs:
        le = LabelEncoder()
        le_data[col] = le.fit_transform(le_data[col])
        encoders[col] = le 

    return le_data, scaler, encoders

def preprocess_test(df, scaler, label_encoder):
    df['Date Time'] = pd.to_datetime(df['Date Time'])
    df['year'] = df['Date Time'].dt.year
    df['month'] = df['Date Time'].dt.month
    df['day'] = df['Date Time'].dt.day
    df['hour'] = df['Date Time'].dt.hour
    df['minute'] = df['Date Time'].dt.minute
    df['second'] = df['Date Time'].dt.second
    df['weekday'] = df['Date Time'].dt.weekday
    df['day_of_year'] = df['Date Time'].dt.dayofyear

    df = df.drop(['Transaction Id', 'Date Time', 'Phone Number', 'CNIC', 'Name', 'Remarks'], axis=1)

    objs = [col for col in df.columns if df[col].dtype == 'O']
    cont_features = ['Amount', 'Old Balance', 'New Balance', 'Service Charges']

    df_scaled = df.copy()
    df_scaled[cont_features] = scaler.transform(df_scaled[cont_features])

    for col in objs:
        df_scaled[col] = label_encoder[col].fit_transform(df_scaled[col])

    return df_scaled




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

    