import requests
import pandas as pd

# -------------------------------
# Step 1: Define API details
# -------------------------------
url = "https://metamorphosis.youv.ai/api/billing/sales-period?user_map_id=70697&start_date=2026-04-01&end_date=2026-04-30"  # Replace with your API endpoint

headers = {
    "Authorization": "Bearer YOUR_API_KEY",  # Replace with your key if needed
    "Accept": "application/json"
}

# -------------------------------
# Step 2: Fetch data from the API
# -------------------------------
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()  # Convert API response to JSON
else:
    print("Failed to fetch data:", response.status_code)
    exit()  # Stop execution if API call fails

# -------------------------------
# Step 3: Convert JSON to DataFrame
# -------------------------------
# If your JSON is a list of dicts:
try:
    df = pd.DataFrame(data)
except ValueError:
    # For nested JSON, normalize it
    df = pd.json_normalize(data)

# Optional: Inspect the DataFrame
print(df.head())

# -------------------------------
# Step 4: Save DataFrame to CSV
# -------------------------------
output_file = "api_data.csv"
df.to_csv(output_file, index=False)
print(f"Data successfully saved to {output_file}")
output_file = "api_data.csv"
df.to_csv(output_file, index=False)