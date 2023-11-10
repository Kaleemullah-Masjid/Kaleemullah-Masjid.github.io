import pandas as pd
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

# Function to Request the API
def request_data_input(year,month):
     # Define latitude and longitude coordinates, and get the current year and month
    lat = 42.03326482384257
    long = -87.73497403508489
    #Example Request:  http://api.aladhan.com/v1/calendar/2017/4?latitude=51.508515&longitude=-0.1254872&method=2
    apiUrl = f'https://api.aladhan.com/v1/calendar/{year}/{month}?latitude={lat}&longitude={long}&school=1;'
    # Perform the HTTP GET request
    req_data = requests.get(apiUrl)
    return(req_data)
def parse_data(response_text):
    # Parse the JSON response and access the 'data' key
    resp_data = json.loads(response_text)['data']
    # Create an empty DataFrame to store prayer times
    df_prayer_times = pd.DataFrame(columns=['Date','Islamic_Date','Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Sunset', 'Maghrib', 'Isha', 'Imsak','Midnight', 'Firstthird', 'Lastthird'])
    # Loop through the data and extract prayer timings and dates
    for a in resp_data:
        prayer_timings = a['timings']
        prayer_dates = a['date']
        # Create a temporary DataFrame from the prayer timings data
        temp_prayer_times = pd.DataFrame.from_dict([prayer_timings])
        # Add a 'Date' column with the human-readable date
        temp_prayer_times['Date'] = prayer_dates['readable']
        temp_prayer_times['Islamic_Date'] = prayer_dates['hijri']['date']
        # Concatenate the temporary DataFrame to the main DataFrame
        df_prayer_times = pd.concat([df_prayer_times,temp_prayer_times])
    return(df_prayer_times)
# Function to convert 24-hour time strings to AM/PM format
def convert_time(pd_series,prayer_name):
    # Split the time strings into parts, extract and convert the time, then format it
    time_parts = pd_series.str.split(' ',expand=True)
    time = time_parts[0]
    #timezone = time_parts[1][1:-1]  # Remove parentheses
    time_parts_list = time.values
    time_parts_list_new = []
    
    for time_ in time_parts_list:
        time_format = "%H:%M"
        # Convert the time string to a datetime object
        dt = datetime.strptime(time_, time_format)
        # Format the datetime object in AM/PM format
        formatted_time = dt.strftime("%I:%M %p")
        time_parts_list_new.append(formatted_time)
    # Create a new DataFrame with the converted time data and set column name to the prayer name
    pd_series_new = pd.DataFrame(time_parts_list_new,columns=[prayer_name])
    
    return pd_series_new
# Function to put prayer times dataframe together
def parse_request(response):
    # Function to handle the API response and display the data
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the content of the response (the web page content)
        prayer_times = parse_data(response.text)
        #GET PRAYER NAMES 
        prayer_names = prayer_times.columns.tolist()[2:]
         # Create a new DataFrame to store prayer times in AM/PM format
        prayer_times_new = pd.DataFrame(columns=prayer_times.columns.to_list())
        # Set the 'Date' column in the new DataFrame
        prayer_times_new['Date'] = prayer_times['Date']
        # Set the 'Date' column in the new DataFrame
        prayer_times_new['Islamic_Date'] = prayer_times['Islamic_Date']
        # Reset the index for the new DataFrame
        prayer_times_new = prayer_times_new.reset_index(drop=True)
        # Convert and replace each prayer time column with the AM/PM format
        for prayer_name in prayer_names:
            time_0 = prayer_times[prayer_name]
            new_time = convert_time(time_0,prayer_name)
            prayer_times_new[prayer_name] = new_time
        # Display the new DataFrame with AM/PM prayer times
        prayer_times_new['Date_Added'] = datetime.today()
        return(prayer_times_new)
    else:
        print(f"Request failed with status code {response.status_code}")
def get_new_data():
    month_next_1 = datetime.today() + relativedelta(months=+1)
    month_next_2 = datetime.today() + relativedelta(months=+2)
    month_next_1_year = month_next_1.year
    month_next_1_month = month_next_1.month

    month_next_2_year = month_next_2.year
    month_next_2_month = month_next_2.month

    temp_data_1 = request_data_input(month_next_1_year,month_next_1_month)
    temp_data_1  = parse_request(temp_data_1)

    temp_data_2 = request_data_input(month_next_2_year,month_next_2_month)
    temp_data_2  = parse_request(temp_data_2)

    temp_data = pd.concat([temp_data_1,temp_data_2])
    return(temp_data)
def combine_data():
    #Function to GET NEXT MONTH & FOLLOWING MONTH DATA
    new_data = get_new_data()

    if new_data is not None:
        file_name = 'PRAYER_TIMES.csv'
        existing_data = pd.read_csv(file_name)
        new_data = new_data[~new_data['Date'].isin(existing_data['Date'])]
        combined_data = pd.concat([new_data, existing_data])
        combined_data.to_csv(file_name, index=False)
def main():
    combine_data()
    
if __name__ == "__main__":
    main()
