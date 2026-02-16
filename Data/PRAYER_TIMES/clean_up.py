import pandas as pd
import os

# get current python file location
current_file_location = os.path.realpath(__file__)
# get file path folder 
current_file_folder = os.path.dirname(current_file_location)

input_file = os.path.join(current_file_folder, "prayer_times.csv")
output_file = os.path.join(current_file_folder, "archive/old_prayer_times.csv")

def clean_prayer_times(input_file, output_file):
    """
    Cleans the prayer times data by removing duplicates and archiving old data.
    """
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Perform cleaning operations (example: drop duplicates)
    df = df.drop_duplicates()
    # Get the current year
    current_year = pd.Timestamp.now().year
    last_year = current_year - 2

    # Date,Islamic_Date,Fajr,Sunrise,Dhuhr,Asr,Sunset,Maghrib,Isha,Imsak,Midnight,Firstthird,Lastthird,Date_Added,Date_New
    
    # if data is from last and older remove
    # date formate 31 Mar 2026
    df['Date_parsed'] = pd.to_datetime(df['Date'], format="%d %b %Y")
    df_old = df[df['Date_parsed'].dt.year <= last_year]
    df_new = df[df['Date_parsed'].dt.year > last_year]
    # drop the parsed date column
    df_old = df_old.drop(columns=['Date_parsed'])
    df_new = df_new.drop(columns=['Date_parsed'])
    # Save the cleaned data to a new file
    df_old.to_csv(output_file, index=False)
    df_new.to_csv(input_file, index=False)

# Call the function
clean_prayer_times(input_file, output_file)
