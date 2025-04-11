import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing

def preprocess(df):
    df['Date Time'] = pd.to_datetime(df['Date Time'])
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
    label_encoder = preprocessing.LabelEncoder()
    le_data=df_normalized

    for col in objs:
        le_data[col]= label_encoder.fit_transform(le_data[col])

    return le_data, scaler, label_encoder

    