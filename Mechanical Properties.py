#This code is to analyze mechanical properties of data from Microtester
#An intellectual property from Chew Lab 
#By Hannah Le on 24-Feb-2025 v.3.0

#Make sure you have the necessary libraries by running pip install in the Terminal

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define the folder path contain all measurements
data_dir = "/Users/littlevanilla/Documents/PhD is fantastic/2024-2025/microtester/D695_remeasurementOLDCAD/400"

# Define the analysis function
def process_files(folder_path):
    # List all CSV files in the folder
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    stiffness = []
    young = []
    max_load = []

    for file in files:
        # Read the CSV file with UTF-8 encoding
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path, encoding="ISO-8859-1")
        
        # Ensure column names are valid
        # df.columns = [col.strip().replace(" ", ".") for col in df.columns]
        
        # Compute new columns
        df['stress'] = df['Force(uN)'] / 2.8  # Column 4 divided by surface area
        df['strain'] = df['Tip Displacement(um)'] / df['Current Size (um)'].iloc[0]  # Column 5 divided by first cell of Column 7
        
        # Filter the data based on the valid strain range
        # Modify these values if you want to get the stiffness values/Young's modulus
        valid_data = df[(df['strain'] >= 0.025) & (df['strain'] <= 0.075)]
        
        # Compute slope over the valid strain range specified above
        if not valid_data.empty:
            slope1, _ = np.polyfit(valid_data['Tip Displacement(um)'],valid_data['Force(uN)'], 1)
            slope2, _ = np.polyfit(valid_data['strain'], valid_data['stress'], 1)
        else:
            slope1, slope2 = np.nan, np.nan  # In case there is no valid data for slope computation
        
        stiffness.append(slope1)
        young.append(slope2)
        
        # Max load (stress)
        load = df['stress'].max()
        max_load.append(load)
        
        # Plot stress vs. strain within the range of strain = 0 - 20%
        filtered_df = df[df['strain'] <= 0.20]
        
        # Save the plot
        plot_file = os.path.join(folder_path, f"plot_{os.path.splitext(file)[0]}.png")
        plt.figure()
        plt.plot(filtered_df['strain'], filtered_df['stress'], 'bo', label='Data points')
        plt.title(f"Stress/strain curve for sample {os.path.basename(file)}")
        plt.xlabel("Strain")
        plt.ylabel("Stress")
        plt.legend()
        plt.savefig(plot_file)
        plt.close()

    # Create the output summary
    report1 = [*stiffness, np.mean(stiffness), np.std(stiffness)]
    report2 = [*max_load, np.mean(max_load), np.std(max_load)]
    report3 = [*young, np.mean(young), np.std(young)]
    output = np.array([report1, report2, report3]).T
    output_df = pd.DataFrame(output, columns=["Stiffness N/m", "Maximum Load N", "Young's Modulus"])
    
    # Write the summary statistics to a CSV file
    output_df.to_csv(os.path.join(folder_path, "Summary_statistics_updated.csv"), index=False, encoding="utf-8-sig")

# # Call the function with the specified data directory
process_files(data_dir)

## Now you just need to check your output files in your folder.
## Good luck with your analysis!
