from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import matplotlib.pyplot as plt

# Load ground truth data (must have same resolution as SAR data)
ground_truth_path = os.getenv('GROUND_TRUTH_PATH')
with rasterio.open(ground_truth_path) as gt_dataset:
    ground_truth = gt_dataset.read(1)

# Ensure ground truth and estimated data align spatially
if ground_truth.shape != soil_moisture_class.shape:
    raise ValueError("Mismatch in spatial dimensions between ground truth and estimated data")

# Calculate statistical metrics
mae = mean_absolute_error(ground_truth.flatten(), soil_moisture_class.flatten())
rmse = np.sqrt(mean_squared_error(ground_truth.flatten(), soil_moisture_class.flatten()))
correlation = np.corrcoef(ground_truth.flatten(), soil_moisture_class.flatten())[0, 1]

print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"Root Mean Square Error (RMSE): {rmse:.4f}")
print(f"Correlation Coefficient (R): {correlation:.4f}")

# Visual Comparison
plt.figure(figsize=(8, 6))
plt.scatter(ground_truth.flatten(), soil_moisture_class.flatten(), alpha=0.5, s=1)
plt.xlabel("Ground Truth Soil Moisture")
plt.ylabel("Estimated Soil Moisture")
plt.title("Scatter Plot: Ground Truth vs. Estimated Soil Moisture")
plt.grid()
plt.show()
