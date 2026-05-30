import requests 
import pandas as pd

url ="https://metamorphosis.youv.ai/api/billing/sales-period?user_map_id=70697&start_date=2026-04-01&end_date=2026-04-30"

resp = requests.get(url)

data = resp.json()

df = pd.DataFrame(data)

print(df.head())