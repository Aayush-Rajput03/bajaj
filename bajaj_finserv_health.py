# -*- coding: utf-8 -*-
"""Bajaj_Finserv_Health.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1i4Me7fXutug8Fdw-zUX2r8JN7CLFGIBM
"""

import pandas as pd
import json
with open('/content/DataEngineeringQ2.json', 'r') as f:
  data = json.load(f)

df = pd.json_normalize(data, max_level=None)

df

df.dtypes

df.isnull()

df.fillna(0)

df.isnull().sum()

df.describe()

df['male'] = df['patientDetails.gender'].apply(lambda x: 1 if x == 'male' else 0)
df['female'] = df['patientDetails.gender'].apply(lambda x: 1 if x == 'female' else 0)
df

def is_valid_phone(number):

  if isinstance(number, str):
    number = number.strip()
    if number.startswith('+91'):
      number = number[3:]
    elif number.startswith('91'):
      number = number[2:]
    if number.isdigit() and 10 <= len(number) <= 10 and 6000000000 <= int(number) <= 9999999999:
      return True
  return False

df['is_valid_phone'] = df['phoneNumber'].apply(is_valid_phone)

# Count the number of valid phone numbers
num_valid_phones = df['is_valid_phone'].sum()

print(f"Number of valid phone numbers: {num_valid_phones}")

correlation = df['patientDetails.birthDate'].corr(df['prescribedMedicines'].str.len())

print(f"Pearson correlation between age and number of prescribed medicines: {correlation}")

def categorize_age(birth_date_str):
  # Assuming birth_date_str is in the format 'YYYY-MM-DDTHH:MM:SS.sssZ'
  from datetime import datetime, date

  # Handle potential None values and non-string types
  if birth_date_str is None or not isinstance(birth_date_str, str):
    return 'Unknown'  # Or any other suitable placeholder

  # Extract date part from timestamp
  birth_date_str = birth_date_str.split('T')[0]

  birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
  today = date.today()
  # Calculate age correctly, accounting for months
  age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
  if age <= 12:
    return 'Child'
  elif 13 <= age <= 19:
    return 'Teen'
  elif 20 <= age <= 59:
    return 'Adult'
  else:
    return 'Senior'

df['ageGroup'] = df['patientDetails.birthDate'].apply(categorize_age)

adult_count = df[df['ageGroup'] == 'Adult']['ageGroup'].count()
print("Count of Adults:", adult_count)