import rasterio
import numpy as np
import matplotlib.pyplot as plt

# File path for the provided GeoTIFF file
# REPLACE with file name
file_path = 's1a-iw-grd-vv-20241015t092718-20241015t092732-056111-06dda4-001-cog.tiff'

def classify_soil_moisture(sar_data, thresholds):
    # Classify soil moisture levels from SAR backscatter using normalized thresholds.
    
    # Parameters:
    # sar_data (ndarray): Normalized SAR backscatter data.
    # thresholds (list): Relative thresholds for classification.
    
    # Returns:
    # ndarray: Soil moisture classification (0 for dry, 1 for moderate, 2 for wet).
 
    soil_moisture_class = np.zeros_like(sar_data, dtype=int)
    soil_moisture_class[sar_data > thresholds[2]] = 2  # Wet soil
    soil_moisture_class[(sar_data > thresholds[1]) & (sar_data <= thresholds[2])] = 1  # Moderate soil
    soil_moisture_class[sar_data <= thresholds[0]] = 0  # Dry soil
    return soil_moisture_class

# Read SAR data from GeoTIFF file
with rasterio.open(file_path) as dataset:
    sar_data = dataset.read(1)

# Normalize SAR data
sar_data_normalized = (sar_data - np.min(sar_data)) / (np.max(sar_data) - np.min(sar_data))

# Define relative thresholds
dry_threshold = np.percentile(sar_data_normalized, 33)  # 33rd percentile for dry
moderate_threshold = np.percentile(sar_data_normalized, 66)  # 66th percentile for moderate
wet_threshold = 1.0  # Maximum value for wet

# Classify soil moisture using the normalized data and thresholds
soil_moisture_class = classify_soil_moisture(sar_data_normalized, [dry_threshold, moderate_threshold, wet_threshold])

# Plot the soil moisture classification map
plt.figure(figsize=(10, 6))
plt.imshow(soil_moisture_class, cmap='Blues', vmin=0, vmax=2)
plt.colorbar(label='Soil Moisture Classification')
plt.title('Soil Moisture Classification (0: Dry, 1: Moderate, 2: Wet)')
plt.xlabel('Pixel X')
plt.ylabel('Pixel Y')
plt.show()
