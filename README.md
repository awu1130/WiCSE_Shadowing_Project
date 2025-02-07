# SAR-Calculations

# Threshold Based:
- Import pre-processed SAR .tiff file into project directory
- Change imported file string to the one you wish to analyze
- Run script to view soil moisture index map

You can run the rest in similar way.


# Pre-processing of SAR image:
Leveraging the Sentinel-1 Toolbox, the preprocessing workflow was tailored to meet the specific requirements of each algorithm, though the following steps outline a general preprocessing pipeline with commonly applied parameters:
1. Read: Load the SAR image and, if needed, resample it to focus on the desired area of interest.
2. Calibration: Configure the parameters to determine whether the output will be in beta0 or sigma0 bands, ensuring accurate radiometric calibration.
3. Terrain Flattening: Smooth or level the terrain to enhance signal readability during processing, leading to more reliable results.
4. Thermal noise removal: Remove unwanted thermal noise to improve image clarity; this step is applied selectively depending on the use case.
5. Terrain Correction: Adjust for distortions caused by elevation changes, producing geometrically accurate images that align with standard map projections, enabling better analysis and usability.
6. Write: Generate the pre-processed image as a Geo TIFF file, making it ready for subsequent SAR-based calculations.
![image](https://github.com/user-attachments/assets/a2ef8238-0ae6-4866-be25-5d7e00f3f5c8)

**Sample image** -![image](https://github.com/user-attachments/assets/3480b6c7-3db7-4e44-b2df-5075ee06f1c9)



