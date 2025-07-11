import numpy as np
import pandas as pd

# FIX: Use correct path for Linux or relative path
# Original Windows path: r"C:\Users\User\Downloads\Study_vs_Score_data.csv"
# Use this instead (assuming the file is in Downloads folder):
df = pd.read_csv("Downloads/Study_vs_Score_data.csv")
# Or if the file is in current directory: df = pd.read_csv("Study_vs_Score_data.csv")

print(df.head())
print(df.columns)

feature1 = df[["Attendance_Hours"]]
target = df["Final_Marks"]

# Importing and training the model 
from sklearn.linear_model import LinearRegression

# FIX: Added parentheses to create an instance of LinearRegression
# Original error: model = LinearRegression (missing parentheses)
model = LinearRegression()  # This is the main fix!
model.fit(feature1, target)

# Making prediction with the model
# Predict marks for a student who studied 4 hours
predicted = model.predict([[4]])
print(f"Predicted marks for 4 hours of study: {predicted[0]:.2f}")