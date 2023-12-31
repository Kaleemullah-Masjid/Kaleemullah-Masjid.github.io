import pandas as pd
import requests
import datetime
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
def request_data():
     # Define latitude and longitude coordinates, and get the current year and month
    lat = 42.03326482384257
    long = -87.73497403508489
    cur_year = datetime.date.today().year
    cur_month = datetime.date.today().month
    cur_month_1 = datetime.date.today().month + 1
    #Example Request:  http://api.aladhan.com/v1/calendar/2017/4?latitude=51.508515&longitude=-0.1254872&method=2
    apiUrl = f'https://api.aladhan.com/v1/calendar/{cur_year}/{cur_month_1}?latitude={lat}&longitude={long}&school=1;'
    # Perform the HTTP GET request
    req_data = requests.get(apiUrl)
    return(req_data)
# Function to parse the JSON data from the API response
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
        dt = datetime.datetime.strptime(time_, time_format)
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
        prayer_times_new['Date_Added'] = datetime.date.today()
        return(prayer_times_new)
    else:
        print(f"Request failed with status code {response.status_code}")
def main():
    i = 0

    for year in range(2020,2024):
        for month in range(1,13):
            if i == 0:
                req_data = request_data_input(year,month)
                req_data  = parse_request(req_data)
                i += 1
            else:
                temp_data = request_data_input(year,month)
                temp_data  = parse_request(temp_data)
                req_data = pd.concat([req_data,temp_data])
                i += 1
    
    # Call the function to handle the API response and display prayer times
    
    # Load the existing DataFrame from the CSV file with "Date" as the index
    #df = pd.read_csv('PRAYER_TIMES.csv')
    #df_new = pd.concat([new_df,df])
    req_data.to_csv('PRAYER_TIMES.csv',index=None)
    
if __name__ == "__main__":
    main()