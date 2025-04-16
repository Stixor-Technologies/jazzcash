
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

class BusinessRules:
    def __init__(self, df):
        self.df = df.copy()
        self.df['Date_Time'] = pd.to_datetime(self.df['Date_Time'], format='%Y-%m-%d %H:%M:%S')

    def rule1_n_transactions_m_minutes(self, max_transactions=3, max_minutes=30):
        flagged = []
        for _, row in self.df.iterrows():
            dt = row['Date_Time']
            recent = self.df[(self.df['Date_Time'] <= dt) & (self.df['Date_Time'] >= dt - pd.Timedelta(minutes=max_minutes))]
            if len(recent) > max_transactions:
                flagged.append(row['Transaction_Id'])
        return flagged

    def rule2_high_risk_cities(self, high_risk=['Sindh', 'Balochistan']):
        flagged = self.df[self.df['Dest_State'].isin(high_risk)]
        return flagged['Transaction_Id'].tolist()

    def rule3_high_risk_region_and_time(self, region='Balochistan', start_time='03:00:00', end_time='04:00:00'):
        flagged = []
        for _, row in self.df.iterrows():
            t = row['Date_Time'].strftime('%H:%M:%S')
            if row['Dest_State'] == region and start_time <= t <= end_time:
                flagged.append(row['Transaction_Id'])
        return flagged

    def rule4_new_account_with_large_transaction(self, amount_thresh=50000, days_thresh=30):
        self.df['Account_Creation_Date'] = pd.to_datetime(self.df['Account_Creation_Date'], errors='coerce')
        cutoff = pd.Timestamp.now() - pd.Timedelta(days=days_thresh)
        flagged = self.df[(self.df['Account_Creation_Date'] >= cutoff) & (self.df['Amount'] > amount_thresh)]
        return flagged['Transaction_Id'].tolist()

    def apply_rules(self, transaction_id=None):
        rules = {
            "BusinessRule1_rule1_n_transactions_m_minutes": self.rule1_n_transactions_m_minutes(),
            "BusinessRule2_rule2_high_risk_cities": self.rule2_high_risk_cities(),
            "BusinessRule3_rule3_high_risk_region_and_time": self.rule3_high_risk_region_and_time(),
            "BusinessRule4_rule4_new_account_with_large_transaction": self.rule4_new_account_with_large_transaction()
        }

        results = {}
        for rule_name, flagged in rules.items():
            results[rule_name] = transaction_id in flagged if transaction_id else False
        return results


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

    def apply_rules(self, transaction_id=None):
        rules = {
            "StatisticalRule5_rule5_large_transaction": self.rule5_large_transaction(),
            "StatisticalRule6_ule6_high_frequency_same_source": self.rule6_high_frequency_same_source(),
            "StatisticalRule7_rule7_unusual_dest_accounts": self.rule7_unusual_dest_accounts(),
            "StatisticalRule8_rule8_time_based_spike": self.rule8_time_based_spike()
        }

        results = {}
        for rule_name, flagged in rules.items():
            results[rule_name] = transaction_id in flagged if transaction_id else False

        return results  # <- ✅ THIS LINE WAS MISSING

