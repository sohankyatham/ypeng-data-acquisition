'''
Power output 
Power (P) = voltage (V) * current (I)

analyzing voltage/current from a Keithley 2601B
Calculate average voltage/current per force


Expand this to finding other key metrics:

peak voltage, peak current
resistance
total energy (joules)
learn abt power density

FIND
max min current
peak current
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Configuration ---
INPUT_CSV_FILE = 'peng_data.csv'

def main():
    """
    Main function to load PENG data, calculate power,
    and plot the results.
    """
    # 1. Load Data
    try:
        df = pd.read_csv(INPUT_CSV_FILE)
    except FileNotFoundError:
        print(f"Error: The file '{INPUT_CSV_FILE}' was not found.")
        print("Please make sure the CSV file is in the same directory as the script.")
        return
    except Exception as e:
        print(f"An error occurred loading the file: {e}")
        return

    # 2. Calculate the Key Metric: Instantaneous Power
    # Power (W) = Voltage (V) * Current (A)
    # We use .abs() because power is generated on both the
    # positive and negative cycles of the vibration.
    df['Power (W)'] = np.abs(df['Voltage (V)'] * df['Current (A)'])
    
    # 3. Find the Peak Power
    # This is the single most important metric for a PENG.
    peak_power_watts = df['Power (W)'].max()
    
    # Convert to a more readable unit, like microwatts (µW)
    peak_power_microwatts = peak_power_watts * 1_000_000
    
    print("\n--- PENG Analysis ---")
    print(f"Successfully loaded {len(df)} data points.")
    print(f"KEY METRIC: Peak Power = {peak_power_microwatts:.2f} µW (microwatts)")

    # 4. Generate the Plot
    plt.figure(figsize=(10, 6))
    
    # Plotting Time vs. Instantaneous Power
    plt.plot(
        df['Time (s)'], 
        df['Power (W)'] * 1_000_000, # Convert to µW for plotting
        marker='o', 
        linestyle='-',
        color='b',
        label='Instantaneous Power'
    )
    
    # Draw a horizontal line for the peak power
    plt.axhline(
        y=peak_power_microwatts, 
        color='r', 
        linestyle='--', 
        label=f'Peak Power: {peak_power_microwatts:.2f} µW'
    )

    # --- Add plot labels and title ---
    plt.title('Piezoelectric Nanogenerator (PENG) Power Output', fontsize=16)
    plt.xlabel('Time (s)', fontsize=12)
    plt.ylabel('Instantaneous Power (µW)', fontsize=12)
    
    plt.legend(fontsize=10)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    # Ensure the layout is tight
    plt.tight_layout()
    
    # 5. Show the plot
    # This will open a new window with your graph.
    print("Showing plot...")
    plt.show()

if __name__ == "__main__":
    main()