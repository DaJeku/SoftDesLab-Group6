import pandas as pd
import matplotlib.pyplot as plt

#dataset
file_path = "breadprice(in).csv"  

df = pd.read_csv(file_path)

#first few rows to verify the dataset
print("Initial Data:")
print(df.head())

# Convert 
if 'Year' in df.columns:
    df['Year'] = df['Year'].astype(int)

# Compute the average bread price per year
# Assuming monthly columns are in index positions 1 onward
if len(df.columns) > 1:
    df['Average Price'] = df.iloc[:, 1:].mean(axis=1)

# Plot the data
plt.figure(figsize=(10, 5))
plt.plot(df['Year'], df['Average Price'], marker='o', linestyle='-', color='orange')
plt.xlabel("Year")
plt.ylabel("Average Bread Price (USD)")
plt.title("Average Price of Bread Over Time")
plt.grid(True)
plt.show()
