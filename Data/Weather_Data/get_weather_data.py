import pandas as pd
import requests
import datetime
import json
import os

# Function to parse the JSON data from the API response
def parse_data(response_text):
    # Parse the JSON response and access the 'data' key
    resp_data = json.loads(response_text)['data']
    # Create an empty DataFrame to store prayer times
    df_prayer_times = pd.DataFrame(columns=['Date','Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Sunset', 'Maghrib', 'Isha', 'Imsak','Midnight', 'Firstthird', 'Lastthird'])
    # Loop through the data and extract prayer timings and dates
    for a in resp_data:
        prayer_timings = a['timings']
        prayer_dates = a['date']
        # Create a temporary DataFrame from the prayer timings data
        temp_prayer_times = pd.DataFrame.from_dict([prayer_timings])
        # Add a 'Date' column with the human-readable date
        temp_prayer_times['Date'] = prayer_dates['readable']
        # Concatenate the temporary DataFrame to the main DataFrame
        df_prayer_times = pd.concat([df_prayer_times,temp_prayer_times])
    return(df_prayer_times)

def get_cur_temp(data):
    temp_1_0_0 = data['number']
    temp_1_0_1 = data['name']
    temp_1_0_2 = data['startTime']
    temp_1_0_3 = data['endTime']
    temp_1_1 = data['temperature']
    temp_1_2 = data['probabilityOfPrecipitation']['value']
    temp_1_3 = data['dewpoint']['value']
    temp_1_4 = data['relativeHumidity']['value']
    temp_1_5 = data['shortForecast']
    temp_data = [temp_1_0_0,temp_1_0_1,temp_1_0_2,temp_1_0_3,temp_1_1,temp_1_2,temp_1_3,temp_1_4,temp_1_5]
    temp_df = pd.DataFrame([temp_data],columns=[['Number','Name','startTime','endTime','Temperature','probabilityOfPrecipitation','dewpoint','relativeHumidity','shortForecast']])
    return(temp_df)



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

def parse_request(response):
    # Function to handle the API response and display the data
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the content of the response (the web page content)
        req_data_txt = json.loads(response.text)
        prayer_times = parse_data(response.text)
        #GET PRAYER NAMES 
        prayer_names = prayer_times.columns.tolist()[1:]
         # Create a new DataFrame to store prayer times in AM/PM format
        prayer_times_new = pd.DataFrame(columns=prayer_times.columns.to_list())
        # Set the 'Date' column in the new DataFrame
        prayer_times_new['Date'] = prayer_times['Date']
        # Reset the index for the new DataFrame
        prayer_times_new = prayer_times_new.reset_index(drop=True)
        # Convert and replace each prayer time column with the AM/PM format
        for prayer_name in prayer_names:
            time_0 = prayer_times[prayer_name]
            new_time = convert_time(time_0,prayer_name)
            prayer_times_new[prayer_name] = new_time
        # Display the new DataFrame with AM/PM prayer times

        prayer_times_new = prayer_times_new.set_index('Date')
        prayer_times_new['Date_Added'] = datetime.date.today()
        return(prayer_times_new)
    else:
        print(f"Request failed with status code {response.status_code}")

def main():
     # Define latitude and longitude coordinates, and get the current year and month

    cur_year = datetime.date.today().year
    cur_month = datetime.date.today().month
    #Example Request:  https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}
    
    with open('api_key.txt') as file:
        api_key = file.readline()
    apiUrl = f'https://api.weather.gov/gridpoints/LOT/71,80/forecast'
    # Perform the HTTP GET request
    #req_data = requests.get(apiUrl)
    #req_data_txt = req_data.text
    #req_data_txt = req_data_txt.strip()
    #req_data_txt = json.loads(req_data_txt)

    with open('weather.json', 'r') as file:
        file_txt = file.read()
        req_data_txt = json.loads(file_txt)

    cur_date = datetime.date.today()
    tmrw_date = cur_date + datetime.timedelta(days=1)
    print(cur_date)
    req_data_txt_0 = get_cur_temp(req_data_txt['properties']['periods'][0])
    req_data_txt_1 = get_cur_temp(req_data_txt['properties']['periods'][1])
    req_data_txt_2 = get_cur_temp(req_data_txt['properties']['periods'][2])
    req_data_txt_3 = get_cur_temp(req_data_txt['properties']['periods'][3])
    req_data_txt_0['Date'] = cur_date
    req_data_txt_1['Date'] = cur_date
    req_data_txt_2['Date'] = tmrw_date
    req_data_txt_3['Date'] = tmrw_date
    req_data_txt_ = pd.concat([req_data_txt_0,req_data_txt_1,req_data_txt_2,req_data_txt_3])

    print(req_data_txt_)

    #with open('weather.json', 'w') as file:
    #    json.dump(req_data_txt,file)
    # Call the function to handle the API response and display prayer times
    #print(apiUrl,r'\n',req_data.text)


if __name__ == "__main__":
    main()