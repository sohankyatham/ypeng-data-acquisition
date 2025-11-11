'''
pyVISA → General instrument control

Keithley 2600 TSP-Python API → Direct scripting interface (preferred for 2601B)

Understand how the current LabVIEW scripts acquire data  - and replicate using Keithley API
'''

'''
Recommendation for now:

Use LabVIEW for data collection and Python for visualization + analysis

Log data into .csv file automatically and LabVIEW drivers handle low-level VISA Communication 

Use LabVIEW to communicate with the Keithley 2601B SourceMeter.
(You will select voltage/current sweep, timing, etc.)

Save the output (voltage, current, time) as a .csv file.

Use Python (NumPy, Pandas, Matplotlib, Streamlit) to:

Read the .csv

Clean and analyze the data

Build plots (voltage vs time, current vs force)

Build a dashboard to visualize experiments in real-time or after recording
'''


import pyvisa
import time

# --- Configuration ---
# IMPORTANT: Replace this with your instrument's actual VISA resource string.
# You can find this using NI MAX, Keysight Connection Expert, or by
# listing resources: `rm.list_resources()`
INSTRUMENT_RESOURCE_STRING = 'GPIB0::24::INSTR'  # Example: GPIB adapter 0, address 24

# Measurement settings
SOURCE_VOLTAGE = 1.0  # Voltage to apply (in Volts)
CURRENT_COMPLIANCE = 0.1  # Current protection limit (in Amps)
NUM_READINGS = 10  # Number of readings to take
READING_INTERVAL = 0.5  # Time between readings (in seconds)

def main():
    """
    Main function to connect, configure, and measure data
    from a Keithley Sourcemeter.
    """
    instrument = None  # Initialize instrument variable
    
    try:
        # 1. Initialize the Resource Manager
        # This searches for available VISA backends (like NI-VISA, Keysight VISA)
        rm = pyvisa.ResourceManager()
        print(f"Available VISA resources: {rm.list_resources()}")

        # 2. Open a connection to the instrument
        print(f"Connecting to: {INSTRUMENT_RESOURCE_STRING}")
        instrument = rm.open_resource(INSTRUMENT_RESOURCE_STRING)

        # Set communication timeouts (optional, but good practice)
        instrument.timeout = 5000  # 5000 ms = 5 seconds
        instrument.read_termination = '\n'
        instrument.write_termination = '\n'

        # 3. Identify the instrument
        # Send the *IDN? query to ask for its identification string
        idn_string = instrument.query('*IDN?')
        print(f"Connected to: {idn_string.strip()}")

        # 4. Configure the Sourcemeter (Keithley SCPI commands)
        
        # Reset the instrument to default settings
        instrument.write('*RST')
        
        # --- Source Configuration ---
        # Set the source function to Voltage
        instrument.write(':SOUR:FUNC VOLT')
        
        # Set the source mode to Fixed (DC) voltage
        instrument.write(':SOUR:VOLT:MODE FIXED')
        
        # Set the source voltage level
        instrument.write(f':SOUR:VOLT:LEV {SOURCE_VOLTAGE}')

        # --- Sense (Measure) Configuration ---
        # Set the sense function to Current
        # Note: "CURR:DC" is often just "CURR"
        instrument.write(':SENS:FUNC "CURR"')
        
        # Set the current protection (compliance)
        instrument.write(f':SENS:CURR:PROT {CURRENT_COMPLIANCE}')
        
        # Enable auto-ranging for the current measurement
        instrument.write(':SENS:CURR:RANG:AUTO ON')

        # Configure the instrument to read Voltage, Current, and Resistance
        # This format is common for models like the 2400 series.
        # It simplifies the data you get back from :READ?
        instrument.write(':FORM:ELEM VOLT, CURR')

        # 5. Turn the output ON
        print("Turning output ON.")
        instrument.write(':OUTP ON')

        # 6. Take Measurements
        print("Starting measurements...")
        readings = []
        
        for i in range(NUM_READINGS):
            # Request a reading from the instrument
            # The :READ? query triggers a measurement and returns the values
            # configured by :FORM:ELEM
            data_string = instrument.query(':READ?')
            
            # The data comes back as a comma-separated string, e.g., "+1.00000E+00,+1.23456E-03"
            voltage_str, current_str = data_string.strip().split(',')
            
            # Convert string values to floating-point numbers
            voltage = float(voltage_str)
            current = float(current_str)
            
            readings.append((voltage, current))
            
            print(f"Reading {i+1}: Voltage={voltage:.6f} V, Current={current:.6E} A")
            
            # Wait for the specified interval
            time.sleep(READING_INTERVAL)

        # 7. Turn the output OFF
        print("Turning output OFF.")
        instrument.write(':OUTP OFF')

        # --- Data Processing ---
        print("\n--- Measurement Complete ---")
        print("Collected Data (Voltage, Current):")
        for v, c in readings:
            print(f"{v:.6f}, {c:.6E}")
            
        # Here, you would typically save `readings` to a CSV file.
        # Example:
        # with open('measurement_data.csv', 'w') as f:
        #     f.write('Voltage (V),Current (A)\n')
        #     for v, c in readings:
        #         f.write(f'{v},{c}\n')
        # print("\nData saved to measurement_data.csv")

    except pyvisa.Error as e:
        # Handle VISA-specific errors
        print(f"A VISA error occurred: {e}")
    except Exception as e:
        # Handle other general errors
        print(f"An error occurred: {e}")
    finally:
        # 8. Always close the connection
        # This block runs whether the try block succeeded or failed
        if instrument:
            print("Closing connection.")
            # Turn output off again, just in case of an error
            try:
                instrument.write(':OUTP OFF')
            except Exception as e:
                print(f"Could not turn off output during cleanup: {e}")
            instrument.close()

if __name__ == "__main__":
    main()