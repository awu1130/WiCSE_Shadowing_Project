import rasterio
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor

# Load the SAR GeoTIFF file
def load_geotiff(file_path):
    with rasterio.open(file_path) as src:
        sar_data = src.read(1)
        profile = src.profile
        return sar_data, profile


# Empirical Relationship (later need to use Water Cloud Model with DEM to derive surface roughness or
# anything else since we don't have ground values)
def estimate_soil_moisture(sar_data):
    sar_data_masked = np.ma.masked_equal(sar_data, 0)
    ground_truth_moisture = 0.5 * sar_data + 20  # A random synthetic relation (not accurate in real-world)

    # Flattening the SAR data and the "ground truth" moisture data to train the model
    sar_data_flat = sar_data_masked.flatten()
    ground_truth_moisture_flat = ground_truth_moisture.flatten()

    # Remove NaNs for regression
    valid_indices = ~np.isnan(sar_data_flat)
    sar_data_flat = sar_data_flat[valid_indices]
    ground_truth_moisture_flat = ground_truth_moisture_flat[valid_indices]

    # Linear Regression
    model = LinearRegression()
    model.fit(sar_data_flat.reshape(-1, 1), ground_truth_moisture_flat)

    # Predict soil moisture
    predicted_soil_moisture = model.predict(sar_data_flat.reshape(-1, 1))

    print(f"SAR data shape: {sar_data.shape}")
    print(f"Valid indices shape: {valid_indices.shape}")

    predicted_soil_moisture_map_flat = np.full_like(sar_data_flat, np.nan)
    predicted_soil_moisture_map_flat[valid_indices] = predicted_soil_moisture
    predicted_soil_moisture_map = predicted_soil_moisture_map_flat.reshape(sar_data.shape)
    return predicted_soil_moisture_map, model


def evaluate_model(ground_truth, predicted):
    mse = mean_squared_error(ground_truth.flatten(), predicted.flatten())
    r2 = r2_score(ground_truth.flatten(), predicted.flatten())
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R-squared: {r2:.2f}")


def visualize_results(sar_data, predicted_soil_moisture):
    # Plot original SAR data
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(sar_data, cmap='gray')
    plt.colorbar(label="SAR Backscatter")
    plt.title("Original SAR Data")

    # Plot predicted soil moisture
    plt.subplot(1, 2, 2)
    plt.imshow(predicted_soil_moisture, cmap='Blues',vmin = 0, vmax = 50)
    plt.colorbar(label="Predicted Soil Moisture (%)")
    plt.title("Predicted Soil Moisture")

    plt.show()

def save_results(predicted_soil_moisture, output_path, profile):
    # Save the predicted soil moisture map as a new GeoTIFF
    with rasterio.open(output_path, 'w', **profile) as dst:
        dst.write(predicted_soil_moisture, 1)
    print(f"Predicted soil moisture map saved to: {output_path}")



# Load SAR data from GeoTIFF file
sar_file_path = 'subset_0_of_S1A_IW_GRDH_1SDV_20241021T083916_20241021T083941_056198_06E122_2806_Cal_TF_tnr_TC.tif'  # Replace with your SAR GeoTIFF path
sar_data, profile = load_geotiff(sar_file_path)
print(sar_data)

# Estimate soil moisture using an empirical model (simple linear regression here)
predicted_soil_moisture, model = estimate_soil_moisture(sar_data)

# Visualize the results
visualize_results(sar_data, predicted_soil_moisture)

#save the results to a new GeoTIFF
output_path = 'predicted_soil_moisture_output.tif'
save_results(predicted_soil_moisture, output_path, profile)