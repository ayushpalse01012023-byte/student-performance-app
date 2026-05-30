import requests
import pandas as pd


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

from xgboost import XGBClassifier


url = "https://metamorphosis.youv.ai/api/billing/sales-period?user_map_id=70697&start_date=2026-04-01&end_date=2026-04-30"
params= {
    "user_map_id": 70697,
    "start_date": "2026-04-01",
    "end_date: ": "2026-04-30"
    }

response = requests.get(url, params = params)
data = response.json()
df = pd.DataFrame(data["data"])
df
df.columns

df = df.drop(columns=[
    'billing_transaction_id',
    'billing_id',
    'invoice_no',
    'receipt_no',
    'remarks'
])
df
df['payment_date'] = pd.to_datetime(df['payment_date'])

df['year'] = df['payment_date'].dt.year
df['month'] = df['payment_date'].dt.month
df['day'] = df['payment_date'].dt.day

df = df.drop(columns=['payment_date'])
df
print(df.dtypes)
label_encoder = LabelEncoder()

categorical_columns = [
    'package_name',
    'patient',
    'staff',
    'status',
    'transaction_type',
    'source',
    'cancellation',
    'sale',
    'payment'
]

for col in categorical_columns:
    df[col] = label_encoder.fit_transform(df[col].astype(str))
    
print(df.dtypes)
X = df.drop(columns=['cancellation'])
y = df['cancellation']

df
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)
model = XGBClassifier()

model.fit(X_train, y_train)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)
new_data = X_test.iloc[0:1]

prediction = model.predict(new_data)

prediction
df
le = LabelEncoder()

df['cancellation'] = le.fit_transform(df['cancellation'])

print(le.classes_)
prediction = model.predict(new_data)

print(le.inverse_transform(prediction))
prediction
