import pandas as pd
from xgboost import XGBRegressor
import pickle

# Load dataset
data = pd.read_csv("data.csv")

# Features & target
X = data[['rainfall','temperature','humidity','fertilizer','soil_type']]
y = data['yield']

# Train model
model = XGBRegressor(n_estimators=200, max_depth=5, learning_rate=0.1)
model.fit(X, y)

# Save model
pickle.dump(model, open("model.pkl", "wb"))

print("Model trained successfully")