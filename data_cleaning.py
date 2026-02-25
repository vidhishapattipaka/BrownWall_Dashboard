import pandas as pd
import numpy as np
import re

# Load dataset
df = pd.read_excel("BROWNWALL TEST FILE.xlsx")

# Standardize column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Clean text columns
text_cols = ['company', 'contact_name', 'sales_person_name', 'location']
for col in text_cols:
    df[col] = df[col].astype(str).str.strip().str.title()

# Clean currency columns
def clean_currency(value):
    if pd.isna(value):
        return 0
    value = str(value)
    value = re.sub(r"[₹, ]", "", value)
    return pd.to_numeric(value, errors="coerce")

df['est_order_value'] = df['est_order_value'].apply(clean_currency)
df['budget'] = df['budget'].apply(clean_currency)

# Convert date column
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Handle missing values
df['location'].fillna("Unknown", inplace=True)
df['lead_source'].fillna("Not Mentioned", inplace=True)

# Remove duplicates
df.drop_duplicates(subset=['company', 'contact_name', 'sales_person_name'], inplace=True)

# Export cleaned data
df.to_csv("cleaned_brownwall_data.csv", index=False)

print("Data cleaning completed successfully!")
