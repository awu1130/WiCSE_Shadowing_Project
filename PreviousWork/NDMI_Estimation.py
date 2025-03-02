import rasterio
import numpy as np
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv()
file_path = os.getenv('FILE_PATH')

if not file_path or not os.path.exists(file_path):
    raise ValueError(f"Invalid file path: {file_path}")

def calculate_ndmi(band1, band2):
    """
    Calculate the Normalized Difference Moisture Index (NDMI)
    NDMI = (NIR - SWIR) / (NIR + SWIR)

    Parameters:
        band1 (ndarray): Near Infrared (NIR) band data
        band2 (ndarray): Shortwave Infrared (SWIR) band data

    Returns:
        ndarray: NDMI values for each pixel
    """
    ndmi = (band1 - band2) / (band1 + band2)
    return np.nan_to_num(ndmi)

def classify_soil_moisture(ndmi):
    """
    Classify soil moisture based on NDMI values

    Parameters:
        ndmi (ndarray): NDMI values

    Returns:
        ndarray: Soil moisture classification (0: Dry, 1: Moderate, 2: Wet)
    """
    soil_moisture_class = np.zeros_like(ndmi, dtype=int)
    soil_moisture_class[ndmi > 1] = 2  # Wet
    soil_moisture_class[(ndmi > -1) & (ndmi < 1)] = 1  # Moderate
    soil_moisture_class[ndmi <= -1] = 0  # Dry
    return soil_moisture_class

# Read GeoTIFF data
with rasterio.open(file_path) as dataset:
    band1 = dataset.read(1)  # Near Infrared (NIR)
    band2 = dataset.read(2)  # Shortwave Infrared (SWIR)

# Normalize the band data
band1_normalized = (band1 - np.min(band1)) / (np.max(band1) - np.min(band1))
band2_normalized = (band2 - np.min(band2)) / (np.max(band2) - np.min(band2))

# Calculate NDMI
ndmi = calculate_ndmi(band1_normalized, band2_normalized)

# Classify soil moisture
soil_moisture_class = classify_soil_moisture(ndmi)

# Plot the NDMI map
plt.figure(figsize=(10, 6))
plt.imshow(ndmi, cmap='RdYlGn', vmin=-1, vmax=1)
plt.colorbar(label='NDMI')
plt.title('Normalized Difference Moisture Index (NDMI)')
plt.xlabel('Pixel X')
plt.ylabel('Pixel Y')
plt.show()

# Plot the soil moisture classification map
plt.figure(figsize=(10, 6))
plt.imshow(soil_moisture_class, cmap='Blues', vmin=0, vmax=2)
plt.colorbar(label='Soil Moisture Classification (0: Dry, 1: Moderate, 2: Wet)')
plt.title('Soil Moisture Classification (0: Dry, 1: Moderate, 2: Wet)')
plt.xlabel('Pixel X')
plt.ylabel('Pixel Y')
plt.show()
