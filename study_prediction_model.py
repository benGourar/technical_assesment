import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Create sample data (since the CSV file path needs to be corrected)
# You can replace this with: df = pd.read_csv("Study_vs_Score_data.csv") 
# when you have the correct file path
np.random.seed(42)
hours = np.random.uniform(20, 80, 100)  # Attendance hours between 20-80
# Create a linear relationship with some noise
marks = 45 + 0.4 * hours + np.random.normal(0, 5, 100)
marks = np.clip(marks, 0, 100)  # Ensure marks are between 0-100

# Create DataFrame
df = pd.DataFrame({
    'Attendance_Hours': hours,
    'Final_Marks': marks
})

print("Dataset Info:")
print(df.head())
print(f"\nDataset shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# Feature and target separation
feature1 = df[["Attendance_Hours"]]  # Note: double brackets to keep as DataFrame
target = df["Final_Marks"]

# Importing and training the model 
# FIX: Added parentheses to instantiate the LinearRegression class
model = LinearRegression()  # This was the main error in your code!
model.fit(feature1, target)

# Making prediction with the model
# Predict marks for a student who studied 4 hours
predicted = model.predict([[4]])
print(f"\nPredicted marks for 4 hours of attendance: {predicted[0]:.2f}")

# Additional predictions for better understanding
test_hours = [10, 20, 30, 40, 50, 60, 70, 80]
for hours in test_hours:
    pred = model.predict([[hours]])
    print(f"Predicted marks for {hours} hours of attendance: {pred[0]:.2f}")

# Model performance
from sklearn.metrics import r2_score, mean_squared_error
y_pred = model.predict(feature1)
r2 = r2_score(target, y_pred)
mse = mean_squared_error(target, y_pred)

print(f"\nModel Performance:")
print(f"R² Score: {r2:.4f}")
print(f"Mean Squared Error: {mse:.4f}")
print(f"Coefficient (slope): {model.coef_[0]:.4f}")
print(f"Intercept: {model.intercept_:.4f}")

# Create a simple visualization
plt.figure(figsize=(10, 6))
plt.scatter(df['Attendance_Hours'], df['Final_Marks'], alpha=0.6, label='Actual Data')
plt.plot(df['Attendance_Hours'], y_pred, color='red', linewidth=2, label='Predicted Line')
plt.xlabel('Attendance Hours')
plt.ylabel('Final Marks')
plt.title('Student Marks vs Attendance Hours Prediction')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('prediction_plot.png', dpi=300, bbox_inches='tight')
plt.show()