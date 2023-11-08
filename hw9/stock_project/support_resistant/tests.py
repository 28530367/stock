from django.test import TestCase

# Create your tests here.
import pandas as pd

data = [
    ["gap", "2022-10-03", "one_signal", 278.99],
    ["gap", "2022-11-09", "one_signal", 273.85],
    ["gap", "2023-02-01", "one_signal", 306.73],
    ["gap", "2023-05-24", "one_signal", 336.67],
    ["bar", "2022-04-25", "one_signal", 329.9],
    ["bar", "2022-04-26", "one_signal", 327.66],
    ["bar", "2022-04-27", "one_signal", 322.88],
    ["bar", "2022-05-02", "one_signal", 318.72],
    ["bar", "2022-05-05", "one_signal", 325.25],
    ["bar", "2022-08-26", "one_signal", 321.51],
    ["bar", "2022-09-13", "one_signal", 303.02],
    ["bar", "2022-09-21", "one_signal", 293.95],
    ["bar", "2022-10-13", "one_signal", 270.17],
    ["bar", "2023-07-20", "one_signal", 384.095],
    ["resistance", "2022-05-27", "one_signal", 306.56],
    ["resistance", "2022-07-19", "one_signal", 296.75],
    ["resistance", "2022-07-29", "one_signal", 314.56],
    ["resistance", "2022-08-12", "one_signal", 330.29],
    ["resistance", "2022-10-25", "one_signal", 284.18],
    ["resistance", "2022-11-11", "one_signal", 284.6],
    ["resistance", "2022-11-30", "one_signal", 293.26],
    ["resistance", "2023-02-01", "one_signal", 296.875],
    ["resistance", "2023-02-02", "one_signal", 311.08],
    ["resistance", "2023-03-16", "one_signal", 304.0],
    ["resistance", "2023-03-30", "one_signal", 315.25],
    ["resistance", "2023-04-28", "one_signal", 321.63],
    ["resistance", "2023-05-18", "one_signal", 334.4209],
    ["resistance", "2023-05-26", "one_signal", 347.87],
    ["resistance", "2023-07-13", "one_signal", 372.85],
    ["resistance", "2023-10-09", "one_signal", 362.95],
    ["neckline", "2022-07-19", "one_signal", 298.3],
    ["neckline", "2023-04-28", "one_signal", 322.56],
    ["neckline", "2023-09-14", "one_signal", 377.27],
    ["neckline", "2023-11-06", "one_signal", 369.21],
    ["neckline", "2023-11-07", "one_signal", 372.7],
    ["gap_resistance", "2023-02-01", "two_signal", 306.73],
    ["resistance_neckline", "2022-07-19", "two_signal", 296.75],
    ["resistance_neckline", "2023-04-28", "two_signal", 321.63]
]

# Create a DataFrame from the list
df = pd.DataFrame(data, columns=['Signal Category', 'Date', 'Signal Name', 'Value'])

# Rename the column 'Signal Name' to 'Signal Type'
df = df.rename(columns={'Signal Name': 'Signal Type'})

# Optionally, convert the 'Date' column to a datetime object
df['Date'] = pd.to_datetime(df['Date'])

# Display the resulting DataFrame
# print(df)

# Create a sample DataFrame
data = {
    "Signal Category": ["gap", "gap", "bar", "bar"],
    "Date": ["2022-10-03", "2022-11-09", "2022-04-25", "2022-04-26"],
    "Signal Type": ["one_signal", "one_signal", "one_signal", "one_signal"],
    "Value": [278.99, 273.85, 329.90, 327.66]
}

df = pd.DataFrame(data)

# Print the original DataFrame
print("Original DataFrame:")
print(df)

# Change the order of columns
df = df[['Signal Type', 'Signal Category', 'Date', 'Value']]

# Print the DataFrame with changed column order
print("\nDataFrame with Changed Column Order:")
print(df)



