import pandas as pd
from collections import deque
import numpy as np
from geopy.distance import geodesic

# Business rules configuration
config = {
        'high_risk_cities' : [101, 202],  # Example high-risk cities
        'high_risk_states' : [10, 12],  # Example high-risk states
        'new_account_threshold' : 10000,  # Account ID threshold for newly created accounts
        'amount_threshold' : 100000,  # Transaction amount threshold
        'n':3,  
        'm' : 5  # Rule 1: 3 transactions in 5 minutes
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
            while (dq[-1] - dq[0]).total_seconds() > config['m'] * 60:
                dq.popleft()
            if len(dq) >= config['n']:
                df.loc[group.index[i], 'flag_rapid_txns'] = 1

    # Rule 2: Flag transactions from/to high-risk cities
    df['flag_high_risk_city'] = df['Source_City'].isin(config['high_risk_cities']) | df['Dest_City'].isin(config['high_risk_cities'])

    # Rule 3: Flag transactions from high-risk region and odd time (e.g., 12 AM - 5 AM)
    df['hour'] = df['timestamp'].dt.hour
    df['flag_risky_time_region'] = ((df['Source_State'].isin(config['high_risk_states'])) & (df['hour'].between(0, 5)))

    # Rule 4: Flag newly created receiving account and large amount
    df['flag_new_acc_large_amt'] = ((df['ID_Dest'].astype(int) > config['new_account_threshold']) & (df['Amount'] > config['amount_threshold']))

    return df