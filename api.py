import requests 
import pandas as pd 
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier 

url = "https://metamorphosis.youv.ai/api/billing/sales-period?user_map_id=70697&start_date=2026-04-01&end_date=2026-04-30"

response = requests.get(url)

data = response.json()
print(data)
print(type(data))
print(data.keys())
for key in data.keys():
    print(key , "->", type(data[key]))
for key in data:
    print(key , type(data[key]))
print(data["data"][0])

df = pd.DataFrame(data["data"])
print(df)

print(df.head())
print(df.isnull().sum())
print(df.select_dtypes(include="object").columns)

