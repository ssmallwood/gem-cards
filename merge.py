import json
import pandas as pd
import numpy as np


# Load the JSON data
def load_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

# Load the CSV data
def load_csv(filename):
    return pd.read_csv(filename)

def merge_data(json_data, csv_data):
    # Use 'Name' from CSV as the key, assuming this matches 'College' in the JSON
    csv_data.set_index('Name', inplace=True)
    
    for college_name, details in json_data.items():
        if college_name in csv_data.index:
            csv_row = csv_data.loc[college_name]
            # Mapping all fields from the CSV to the JSON structure
            details['UNITID'] = csv_row['UNITID']
            details['Four Year Cost'] = csv_row['Four Year Cost']
            details['Earnings to Price Ratio'] = csv_row['Earnings to Price Ratio']
            details['Earnings 10 Years Post-Entry'] = csv_row['Earnings 10 Years Post-Entry 2008-2009 + 2009-2010 Cohorts (Bain)']
            details['Earnings Residual (Bain)'] = csv_row['Earnings Residual (Bain)']
            details['FTFT Grad Rate (6 Years)'] = csv_row['FTFT Grad Rate (6 Years) 2015-2016 Cohort (Bain)']
            details['Grad Rates Residual (Bain)'] = csv_row['Grad Rates Residual (Bain)']
            details['City'] = csv_row['City']
            details['State'] = csv_row['State']
            details['ZIP code'] = csv_row['ZIP code (HD2022)']
            details['Carnegie Classification 2021'] = csv_row['Carnegie Classification 2021: Basic (HD2022)']
            details['Control'] = csv_row['Control']
            details['Grand total Grad Rate Cohort'] = csv_row['Grand total Grad Rate Cohort (IPEDS)']
            details['Grand total Completers'] = csv_row['Grand total Completers 22 (IPEDS)']
            details['Graduation Rate'] = csv_row['Graduation Rate']
            details['Undergrads Fall 2022'] = csv_row['Undergrads Fall 2022 (IPEDS)']
            details['Applicants 2022'] = csv_row['Applicants 2022 (IPEDS)']
            details['Admits 2022'] = csv_row['Admits 2022 (IPEDS)']
            details['Enrolled 2022'] = csv_row['Enrolled 2022 (IPEDS)']
            details['Admission Rate'] = csv_row['Admission Rate']
            details['Yield Rate'] = csv_row['Yield Rate']
            details['Latitude'] = csv_row['Latitude']
            details['Longitude'] = csv_row['Longitude']
            details['Institution Type'] = csv_row['Institution Type']
            details['Rating'] = csv_row['Rating']
            details['Tagged'] = csv_row['Tagged']
        else:
            print(f"College {college_name} not found in CSV data.")


def my_converter(obj):
    """Converts numpy types to Python standard types."""
    if isinstance(obj, (np.integer, np.floating)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.bool_):
        return bool(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def save_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, default=my_converter, indent=4)

def main():
    json_file = 'full_college_data.json'  # Update path as needed
    csv_file = 'rated_tagged_colleges.csv'  # Update path as needed
    output_json_file = 'updated_college_data.json'  # Update path as needed

    json_data = load_json(json_file)
    csv_data = load_csv(csv_file)
    merge_data(json_data, csv_data)
    save_json(json_data, output_json_file)

if __name__ == "__main__":
    main()
