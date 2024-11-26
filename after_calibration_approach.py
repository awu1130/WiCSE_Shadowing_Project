import h5py
import numpy as np
import rasterio
from rasterio.enums import Resampling
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Load the HDF5 file
smap_file_path = '79569101/SMAP_L3_SM_AP_20150601_R13080_001.h5'
with h5py.File(smap_file_path, 'r') as hdf:
    # Access the soil moisture dataset
    soil_moisture_data = hdf['Soil_Moisture_Retrieval_Data/soil_moisture'][:]

# Load the SAR GeoTIFF file
sar_file_path = 'subset_0_of_S1A_IW_GRDH_1SDV_20241021T083916_20241021T083941_056198_06E122_2806_Cal_TF_tnr_TC.tif'  # Replace with your SAR GeoTIFF file path
# Load the SAR GeoTIFF data
with rasterio.open(sar_file_path) as src:
    sar_data = src.read(1)  # Read the first band
    print("SAR Data Shape:", sar_data.shape)

# Ensure dimensions match
if sar_data.shape != soil_moisture_data.shape:
    # Resample SAR data to match SMAP resolution
    new_shape = soil_moisture_data.shape

    # Resample the SAR data using bilinear resampling
    with rasterio.open(sar_file_path) as src:
        sar_resampled = src.read(
            out_shape=new_shape,
            resampling=Resampling.bilinear
        )
else:
    sar_resampled = sar_data

# Now create a valid mask for the soil moisture data
valid_mask = ~np.isnan(soil_moisture_data)

# Ensure the valid mask is the same shape as the resampled SAR data
print(sar_resampled.shape, valid_mask.shape)
if sar_resampled.shape != valid_mask.shape:
    print(f"Warning: SAR resampled shape {sar_resampled.shape} does not match valid mask shape {valid_mask.shape}.")


# Apply the mask to the resampled SAR data
sar_valid = sar_resampled[1][valid_mask]
sm_valid = soil_moisture_data[valid_mask]

# Fit a linear regression model
model = LinearRegression()
model.fit(sar_valid.reshape(-1, 1), sm_valid)

# Get the coefficients
a = model.coef_[0]
b = model.intercept_

# Print the coefficients
print(f'Calibration Coefficient a: {a}')
print(f'Calibration Coefficient b: {b}')

# Plot the results
plt.scatter(sar_valid, sm_valid, color='blue', label='Data Points')
plt.plot(sar_valid, model.predict(sar_valid.reshape(-1, 1)), color='red', label='Fitted Line')
plt.xlabel('SAR Backscatter Coefficient (σ0)')
plt.ylabel('Ground Truth Soil Moisture')
plt.legend()
plt.title('SAR Backscatter vs. Soil Moisture')
plt.show()

# Estimate soil moisture using the derived coefficients
estimated_soil_moisture = a * sar_data + b

# Visualize the estimated soil moisture
plt.imshow(estimated_soil_moisture, cmap='Blues', vmin=-10000, vmax=-9000)

plt.colorbar(label='Estimated Soil Moisture')
plt.title('Estimated Soil Moisture from SAR Data')
plt.show()

# Update the profile for the new file
#sar_profile.update(dtype=rasterio.float32, count=1)

# Write the estimated soil moisture to a new GeoTIFF
#output_file_path = 'estimated_soil_moisture.tif'
#with rasterio.open(output_file_path, 'w', **sar_profile) as dst:
#    dst.write(estimated_soil_moisture.astype(rasterio.float32), 1)
