from sklearn.model_selection import train_test_split
from SetCreator import create_set
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt

st = create_set("SPY", False)

df = st[['DATE', 'CLOSE_PRICE', '15_EMA']]
X_train, X_test, y_train, y_test = train_test_split(df[['CLOSE_PRICE']], df[['15_EMA']], test_size=.2)

model = LinearRegression()
# Train the model
model.fit(X_train, y_train)
# Use model to make predictions
y_pred = model.predict(X_test)

plt.figure(figsize=(15,5))
plt.plot(df['DATE'],df['CLOSE_PRICE'])
plt.plot(df['DATE'],df['15_EMA'])
plt.show()

print(y_pred.transpose())

# Printout relevant metrics
print("Model Coefficients:", model.coef_)
print("Mean Absolute Error:", mean_absolute_error(y_test, y_pred))
print("Coefficient of Determination:", r2_score(y_test, y_pred))




