import csv
from datetime import datetime

def write_betting_data_to_csv(data_list):
    # Get the current date in the format YYYY-MM-DD
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Define the filename with the date
    filename = f'raw_temp_{current_date}.csv'
    
    # Define the header for the CSV
    header = ['outcome_1', 'odds_1', 'outcome_2', 'odds_2', 'site', 'time_found']
    
    # Open the CSV file to write the data
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        
        # Write the header
        writer.writeheader()
        
        # Write the rows of data
        for data in data_list:
            writer.writerow(data)
    
    print(f"CSV file '{filename}' written successfully!")