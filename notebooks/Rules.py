import pandas as pd
from datetime import datetime, timedelta

# -------------------------------
# Business Rules Class
# -------------------------------
class BusinessRules:
    def __init__(self, df):
        self.df = df.copy()
        self.df['Date_Time'] = pd.to_datetime(self.df['Date_Time'], format='%Y-%m-%d %H:%M:%S')

    def rule1_n_transactions_m_minutes(self, max_transactions=3, max_minutes=30):
        flagged = []
        for _, row in self.df.iterrows():
            dt = row['Date_Time']
            recent = self.df[(self.df['Date_Time'] <= dt) & (self.df['Date_Time'] >= dt - timedelta(minutes=max_minutes))]
            if len(recent) > max_transactions:
                flagged.append(row['Transaction_Id'])
        return flagged

    def rule2_high_risk_cities(self, high_risk=['Sindh', 'Balochistan']):
        flagged = self.df[self.df['Dest_State'].isin(high_risk)]
        return flagged['Transaction_Id'].tolist()

    def rule3_high_risk_region_and_time(self, region='Balochistan', times=['03:00:00', '04:00:00']):
        flagged = []
        for _, row in self.df.iterrows():
            t = row['Date_Time'].strftime('%H:%M:%S')
            if row['Dest_State'] == region and t in times:
                flagged.append(row['Transaction_Id'])
        return flagged

    def rule4_new_account_with_large_transaction(self, amount_thresh=50000, days_thresh=30):
        self.df['Account_Creation_Date'] = pd.to_datetime(self.df['Account_Creation_Date'], errors='coerce')
        cutoff = datetime.now() - timedelta(days=days_thresh)
        flagged = self.df[(self.df['Account_Creation_Date'] >= cutoff) & (self.df['Amount'] > amount_thresh)]
        return flagged['Transaction_Id'].tolist()

# -------------------------------
# Statistical Rules Class
# -------------------------------
class StatisticalRules:
    def __init__(self, df):
        self.df = df.copy()
        self.df['Date_Time'] = pd.to_datetime(self.df['Date_Time'])

    def rule5_large_transaction(self, threshold=100000):
        return self.df[self.df['Amount'] > threshold]['Transaction_Id'].tolist()

    def rule6_high_frequency_same_source(self, max_txn=5):
        flagged = []
        for _, group in self.df.groupby('IMEI'):
            if len(group) > max_txn:
                flagged.extend(group['Transaction_Id'].tolist())
        return flagged

    def rule7_unusual_dest_accounts(self, unusual=['XYZ123', 'PQR999']):
        return self.df[self.df['ID_Dest'].isin(unusual)]['Transaction_Id'].tolist()

    def rule8_time_based_spike(self, hour=12, threshold=5):
        self.df['Hour'] = self.df['Date_Time'].dt.hour
        counts = self.df[self.df['Hour'] == hour].groupby('IMEI').size()
        spiked = counts[counts > threshold].index
        flagged = self.df[(self.df['IMEI'].isin(spiked)) & (self.df['Hour'] == hour)]
        return flagged['Transaction_Id'].tolist()

# -------------------------------
# Apply All Rules Class
# -------------------------------
class FraudRulesEngine:
    def __init__(self, df):
        self.df = df
        self.business = BusinessRules(df)
        self.statistical = StatisticalRules(df)

    def apply_all_rules(self):
        results = {
            'Rule1': self.business.rule1_n_transactions_m_minutes(),
            'Rule2': self.business.rule2_high_risk_cities(),
            'Rule3': self.business.rule3_high_risk_region_and_time(),
            'Rule4': self.business.rule4_new_account_with_large_transaction(),
            'Rule5': self.statistical.rule5_large_transaction(),
            'Rule6': self.statistical.rule6_high_frequency_same_source(),
            'Rule7': self.statistical.rule7_unusual_dest_accounts(),
            'Rule8': self.statistical.rule8_time_based_spike()
        }

        # Combine all flagged transactions (deduplicated)
        all_flagged = list(set(txn for txns in results.values() for txn in txns))

        return {
            'flagged_by_rule': results,
            'combined_flagged_transactions': all_flagged
        }
