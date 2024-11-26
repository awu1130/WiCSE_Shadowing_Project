import h5py
import numpy as np
import matplotlib.pyplot as plt


# Path to your SMAP Level 3 HDF5 file
file_path = '79569101/SMAP_L3_SM_AP_20150601_R13080_001.h5'

# Open the SMAP HDF5 file to explore its structure
with h5py.File(file_path, 'r') as f:
    # Print all the keys (groups and datasets)
    print("Keys in the HDF5 file:")
    print(list(f.keys()))

    if 'Soil_Moisture_Retrieval_Data' in f:
        print("Soil Moisture Data Groups:")
        print(list(f['Soil_Moisture_Retrieval_Data'].keys()))

    if 'Soil_Moisture_Retrieval_Data' in f:
        soil_moisture = f['Soil_Moisture_Retrieval_Data/soil_moisture'][:]
        latitudes = f['Soil_Moisture_Retrieval_Data/latitude'][:]
        longitudes = f['Soil_Moisture_Retrieval_Data/longitude'][:]
        print(f['Soil_Moisture_Retrieval_Data/retrieval_qual_flag'])
        # Check if the quality flag exists
        if 'retrieval_qual_flag' in f['Soil_Moisture_Retrieval_Data']:
            quality_flag = f['Soil_Moisture_Retrieval_Data/retrieval_qual_flag'][:]
            print("here")
        else:
            print(soil_moisture)
            quality_flag = np.ones_like(soil_moisture)  # If no quality flag, assume all data is valid

        # Print out the dimensions of the extracted data
        print(f"Shape of soil moisture data: {soil_moisture.shape}")
        print(f"Shape of latitudes: {latitudes.shape}")
        print(f"Shape of longitudes: {longitudes.shape}")
        print(f"Shape of quality flag: {quality_flag.shape}")
        print(quality_flag)
        print("Unique values in quality flag:", np.unique(quality_flag))
    # Example filtering: Keep only the data with good quality
valid_mask = (quality_flag == 0) | (quality_flag == 1)
valid_soil_moisture = soil_moisture[valid_mask]
valid_latitudes = latitudes[valid_mask]
valid_longitudes = longitudes[valid_mask]

# Plotting the filtered soil moisture data on a map
plt.figure(figsize=(10, 6))
plt.scatter(valid_longitudes, valid_latitudes, c=valid_soil_moisture, cmap='viridis', s=1)
plt.colorbar(label='Soil Moisture (%)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('SMAP Soil Moisture Data (Good Quality)')
plt.show()