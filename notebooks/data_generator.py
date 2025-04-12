import pandas as pd
import random
import string
from datetime import datetime, timedelta
import numpy as np
from sklearn.model_selection import train_test_split


class Data():

    def __init__(self,path = '', data_name = 'original'):
        
        self.data_name = data_name
        if self.data_name == 'original':
            
            try:
                
                self.df = pd.read_csv(path)
                self.df = self.df.drop(['step','oldbalanceDest','newbalanceDest' ,'isFlaggedFraud'],axis = 1)
                self.num_rows = len(self.df) 
                self.df.rename(columns={
                    'type': 'Type',
                    'amount': 'Amount',
                    'nameOrig': 'ID Source',
                    'oldbalanceOrg': 'Old Balance',
                    'newbalanceOrig': 'New Balance',
                    'nameDest': 'ID Dest',
                    'isFraud': 'Is Fraud'
                }, inplace=True)
            except:
                print("Path not found!")
        elif self.data_name == 'fraud':
            try: 
                self.df = None

            except:
                print("Unable to Generate Data")

    def add_timestamps(self,range_year):

        def random_datetime():
            year = random.randint(range_year[0], range_year[1])
            month = random.randint(1, 12)
            day = random.randint(1, 28)  # To avoid invalid days in February
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            return datetime(year, month, day, hour, minute, second)
        

        timestamps = []

        current_time = random_datetime()
        timestamps.append(current_time)

        for _ in range(self.num_rows - 1):
            gap = random.randint(1, 10)  # Random gap in seconds
            current_time += timedelta(seconds=gap)
            
            # With a small chance, jump to a completely new random date
            if random.random() < 0.1:  # 10% chance to reset to new random date
                current_time = random_datetime()
            
            timestamps.append(current_time)

        # Convert to string format
        timestamp_strings = [ts.strftime('%Y-%m-%d %H:%M:%S') for ts in timestamps]
        self.df['Date Time'] = timestamp_strings

    def add_states_cities(self,pakistan_city_state):

        cities = []
        states = []

        for _ in range(self.num_rows):
            state = random.choice(list(pakistan_city_state.keys()))
            city = random.choice(pakistan_city_state[state])
            states.append(state)
            cities.append(city)

        # Add to your existing DataFrame
        self.df['Source State'] = states
        self.df['Source City'] = cities    


        cities = []
        states = []

        for _ in range(self.num_rows):
            state = random.choice(list(pakistan_city_state.keys()))
            city = random.choice(pakistan_city_state[state])
            states.append(state)
            cities.append(city)

        # Add to your existing DataFrame
        self.df['Dest State'] = states
        self.df['Dest City'] = cities

    def add_transaction_ids(self):

        def generate_transaction_id(existing_ids):
            while True:
                transaction_id = ''.join(random.choices(string.digits, k=10))
                if transaction_id not in existing_ids:
                    existing_ids.add(transaction_id)
                    return transaction_id

        # Set to track already used transaction IDs
        used_ids = set()

        # Generate unique transaction IDs
        transaction_ids = [generate_transaction_id(used_ids) for _ in range(self.num_rows)]

        # Add the 'transaction_id' column to the existing DataFrame
        self.df['Transaction Id'] = transaction_ids

    def add_devices(self,device_models):
        def generate_device_name():
            device_number = random.randint(1, 10)  # Random device number (1 to 10)
            return f"Device {device_number}"

        def generate_device_model():
            return random.choice(device_models)  # Choose a random device model

        # Choose between Option 1 and Option 2
        use_generic_device_names = False  # Set to False to use Option 2

        # Generate synthetic device names for each row in the DataFrame
        device_names = []

        for _ in range(self.num_rows):  # Assuming your DataFrame is 'df'
            if use_generic_device_names:
                device_names.append(generate_device_name())  # Option 1: "Device 1", "Device 2", etc.
            else:
                device_names.append(generate_device_model())  # Option 2: iPhone 13, Samsung Galaxy, etc.

        # Add the 'device_name' column to the DataFrame
        self.df['Device Name'] = device_names

    def add_imeis(self):
        def generate_imei():
            imei_body = ''.join(random.choices('0123456789', k=14))  # Generate first 14 digits
            imei_check_digit = luhn_check_digit(imei_body)  # Calculate check digit
            return imei_body + str(imei_check_digit)

        # Luhn Algorithm to calculate check digit
        def luhn_check_digit(imei_body):
            total = 0
            reversed_digits = imei_body[::-1]
            
            for i, digit in enumerate(reversed_digits):
                n = int(digit)
                if i % 2 == 1:
                    n *= 2
                    if n > 9:
                        n -= 9
                total += n
            
            check_digit = (10 - (total % 10)) % 10
            return check_digit

        # Generate synthetic IMEIs for each row in the DataFrame
        imeis_list = []

        for _ in range(self.num_rows):  # Loop over each user (row)
            # Generate a single IMEI for each row (user)
            imei = generate_imei()
            imeis_list.append(imei)

        # Add the IMEI column with one IMEI per user
        self.df['IMEI'] = imeis_list

    def add_phone_numbers(self):

        def generate_phone_number():
            # Pakistan country code: +92
            country_code = "+92"
            
            # Generate the first 3 digits (between 300 and 350)
            first_three = random.randint(300, 350)
            
            # Generate the rest of the phone number (7 digits)
            phone_number = ''.join(random.choices('0123456789', k=7))
            
            # Combine the country code and the phone number
            full_phone_number = f"{country_code} {first_three}-{phone_number[:4]}{phone_number[4:]}"
            return full_phone_number

        # Generate a random phone number for each row in the DataFrame
        phone_numbers = [generate_phone_number() for _ in range(self.num_rows)]

        # Add the 'phone_number' column to the DataFrame
        self.df['Phone Number'] = phone_numbers

    def add_names_cnics(self,names):
        def generate_cnic():
            first_part = random.randint(10000, 99999)  # 5 digits
            second_part = random.randint(1000000, 9999999)  # 7 digits
            last_digit = random.randint(0, 9)  # 1 digit
            return f"{first_part}-{second_part}-{last_digit}"

        # Function to generate a random name
        def generate_name():
            first_name = random.choice(names['first_names'])
            last_name = random.choice(names['last_names'])
            return f"{first_name} {last_name}"

        # Generate CNIC and Name for each row in the DataFrame
        cnic_list = [generate_cnic() for _ in range(self.num_rows)]
        name_list = [generate_name() for _ in range(self.num_rows)]

        # Add the CNIC and Name columns to the DataFrame
        self.df['CNIC'] = cnic_list
        self.df['Name'] = name_list

    def add_kyc(self,kyc_status_options):
        def generate_kyc_status():
            return random.choice(kyc_status_options)
    

        # Generate random KYC status for each row in the DataFrame
        kyc_status_list = [generate_kyc_status() for _ in range(self.num_rows)]

        # Add the 'KYC status' column to the DataFrame
        self.df['KYC Status'] = kyc_status_list

    def add_service_charges(self):
        def calculate_service_charge(amount):
            return amount * 0.002  # 2% service charge

        self.df['Service Charges'] = self.df['Amount'].apply(calculate_service_charge)
    
    def add_narations(self,narrations):
        

        # Function to randomly assign narration or leave it empty
        def generate_narration():
            if random.random() < 0.5:  # 80% chance to have a narration
                return random.choice(narrations)
            else:
                return ""  # 20% chance to leave it empty

        # Add the 'Narration/Remarks' column to the DataFrame
        self.df['Remarks'] = [generate_narration() for _ in range(self.num_rows)]

    def order_columns(self,new_column_order):
        
        # Reorder the columns
        self.df = self.df[new_column_order]

    def add_channels(self,channel_options):
        def generate_channel():
            return random.choice(channel_options)
        
        self.df['Channel'] = [generate_channel() for _ in range(self.num_rows)]

    def generate_columns(self):
        
        city_state = {
            'Punjab': [
                'Lahore', 'Rawalpindi', 'Multan', 'Faisalabad', 'Sialkot', 'Gujranwala',
                'Bahawalpur', 'Dera Ghazi Khan', 'Rahim Yar Khan', 'Sargodha', 'Sheikhupura', 'Okara', 'Jhelum'
            ],
            'Sindh': [
                'Karachi', 'Hyderabad', 'Sukkur', 'Larkana', 'Nawabshah', 'Mirpur Khas', 'Thatta', 'Dadu', 'Jacobabad'
            ],
            'Khyber Pakhtunkhwa': [
                'Peshawar', 'Abbottabad', 'Swat', 'Mardan', 'Kohat', 'Bannu', 'Dera Ismail Khan', 'Charsadda', 'Nowshera'
            ],
            'Balochistan': [
                'Quetta', 'Gwadar', 'Khuzdar', 'Turbat', 'Sibi', 'Zhob', 'Loralai', 'Chaman', 'Dera Bugti'
            ],
            'Islamabad Capital Territory': [
                'Islamabad'
            ],
            'Gilgit-Baltistan': [
                'Gilgit', 'Skardu', 'Hunza', 'Ghanche', 'Astore'
            ],
            'Azad Kashmir': [
                'Muzaffarabad', 'Mirpur', 'Rawalakot', 'Kotli', 'Bagh'
            ]
        }

        devices = ['iPhone 13', 'Samsung Galaxy S21', 'OnePlus 9', 'Google Pixel 6', 'Xiaomi Mi 11']

        names = {'first_names' : ['Ahmed', 'Ali', 'Hassan', 'Imran', 'Zain', 'Sara', 'Ayesha', 'Fatima', 'Nida', 'Usman', 
                    'Bilal', 'Khalid', 'Raheel', 'Sana', 'Muneeb', 'Nashit', 'Samina', 'Fariha', 'Maira', 'Rida']
                    , 
                    'last_names' : ['Khan', 'Ahmed', 'Ali', 'Shah', 'Qureshi', 'Rana', 'Bhatti', 'Javed', 'Iqbal', 'Siddiqui',
                    'Butt', 'Khalid', 'Hashmi', 'Mirza', 'Mughal', 'Anwar', 'Jamil', 'Farooq', 'Rizvi', 'Chaudhry']
        }

        kyc_status_options = ["Validated", "Registered", "On-Hold", "Under Process"]
        
        narrations = [
            "Food purchase",
            "Payment for services",
            "Online shopping",
            "Mobile recharge",
            "Payment for groceries",
            "Restaurant bill",
            "Travel ticket booking",
            "Utility bill payment",
            "Subscription fee",
            "Entertainment purchase",
            "Charity donation",
            "Cash withdrawal",
            "Online gaming purchase"
        ]

        new_column_order = ['Transaction Id', 'Date Time', 'Phone Number', 'CNIC', 'Name','Type', 'Amount', 'ID Source', 'Old Balance', 'New Balance',
         'Source State', 'Source City', 
       'Device Name', 'IMEI',  'KYC Status',
       'Service Charges', 'Channel', 'Remarks' , 'ID Dest', 'Dest State', 'Dest City', 'Is Fraud']

        channels = [
            "Bank Transfer", 
            "Credit Card", 
            "Debit Card", 
            "E-Wallet", 
            "Mobile Payments"
        ]

        self.add_transaction_ids()    
        self.add_timestamps((2019,2025))
        self.add_states_cities(city_state)
        self.add_channels(channels)
        
        self.add_devices(devices)
        self.add_imeis()
        self.add_phone_numbers()
        self.add_names_cnics(names)
        self.add_kyc(kyc_status_options)

        self.add_service_charges()
        self.add_narations(narrations)
        self.order_columns(new_column_order)

    def save_data(self,path):
        self.df.columns = (
            self.df.columns
            .str.strip()
            .str.lower()
            .str.replace(' ', '_')
            .str.replace('-', '_')
        )
        self.df.to_csv(path, index = False)

    def show(self):
        print(self.df)

    def get(self):
        return self.df
    
    def replace_data(self,new_data):
        
        self.df = new_data
        
    def split_data(self, test_size = 0.3):
        train_df, test_df = train_test_split(self.df, test_size=test_size, random_state=10)

        return train_df, test_df

    def add_fraud_rows(self,num_records):
        
        if self.data_name == 'fraud':
            
            transfer_cashout_ratio = 0.5
            zero_out_ratio = 0.7  # 10% of transactions will zero out the balance

            def generate_customer_id():
                return "C" + str(random.randint(100000000, 1999999999))

            data = []

            for _ in range(int(num_records * transfer_cashout_ratio // 2)):
                should_zero_out = random.random() < zero_out_ratio

                if should_zero_out:
                    old_balance_sender = round(random.uniform(100.0, 2000000.0), 2)
                    amount = old_balance_sender
                    new_balance_sender = 0.0
                else:
                    amount = round(random.uniform(100.0, 2000000.0), 2)
                    old_balance_sender = round(random.uniform(amount + 100, amount + 100000), 2)
                    new_balance_sender = round(old_balance_sender - amount, 2)

                # Middle account (same logic)
                should_zero_out_mid = random.random() < zero_out_ratio

                if should_zero_out_mid:
                    old_balance_middle = round(random.uniform(100.0, 2000000.0), 2)
                    amount_middle = old_balance_middle
                    new_balance_middle = 0.0
                else:
                    amount_middle = amount  # Keep it same to maintain logical TRANSFER + CASH_OUT pair
                    old_balance_middle = round(random.uniform(amount + 100, amount + 100000), 2)
                    new_balance_middle = round(old_balance_middle - amount, 2)

                sender = generate_customer_id()
                middle_account = generate_customer_id()
                receiver = generate_customer_id()

                data.append(["TRANSFER", amount, sender, middle_account, old_balance_sender, new_balance_sender])
                data.append(["CASH_OUT", amount_middle, middle_account, receiver, old_balance_middle, new_balance_middle])

            # Generate remaining unpaired transactions
            for _ in range(num_records - len(data)):
                txn_type = random.choice(["TRANSFER", "CASH_OUT"])
                should_zero_out = random.random() < zero_out_ratio

                if should_zero_out:
                    old_balance = round(random.uniform(100.0, 2000000.0), 2)
                    amount = old_balance
                    new_balance = 0.0
                else:
                    amount = round(random.uniform(100.0, 2000000.0), 2)
                    old_balance = round(random.uniform(amount + 100, amount + 100000), 2)
                    new_balance = round(old_balance - amount, 2)

                nameOrig = generate_customer_id()
                nameDest = generate_customer_id()

                data.append([txn_type, amount, nameOrig, nameDest, old_balance, new_balance])

            # Shuffle and save
            random.shuffle(data)
            self.df = pd.DataFrame(data, columns=["Type", "Amount", "ID Source", "ID Dest", "Old Balance", "New Balance"])

            self.num_rows = num_records 
            self.df['Is Fraud'] = 1

            self.generate_columns()
        else:
            print("Original dataset is being used. Cant create fraud entries generate seperate data and then concatenate")

    def concat_data(self,new_data):
        try:

            merged_data = pd.concat([self.df, new_data], axis=0, ignore_index=True)

            # Shuffle the merged dataset
            self.df = merged_data.sample(frac=1).reset_index(drop=True)
        except:
            print("Columns Mismatched!")




                















