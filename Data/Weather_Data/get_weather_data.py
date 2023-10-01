import pandas as pd
import requests
import datetime
import json
import os

# Function to parse the JSON data from the API response
def parse_data(response_text):
    # Parse the JSON response and access the 'data' key
    req_data_txt = json.loads(response_text)['properties']['periods']

    #Load JSON Data INTO PANDAS DF
    df = pd.DataFrame(req_data_txt)
    #NORMALIZE JSON COLS
    df_temp_1 = pd.json_normalize(df['probabilityOfPrecipitation'])['value']
    df_temp_2 = pd.json_normalize(df['dewpoint'])['value']
    df_temp_3 = pd.json_normalize(df['relativeHumidity'])['value']
    #DROP ORIGINAL COLS
    df = df.drop(columns=['probabilityOfPrecipitation','dewpoint','relativeHumidity','number','icon'])

    #SET NEW COLS TO PARSED DATED
    df['probabilityOfPrecipitation'] = df_temp_1
    df['dewpoint'] = df_temp_2
    df['relativeHumidity'] = df_temp_3
    #DROP TEMP DATA
    df_temp_1=''
    df_temp_2=''
    df_temp_3=''
    #Parse Date
    df['startTime'] = pd.to_datetime(df.startTime)
    df['endTime'] = pd.to_datetime(df.endTime)
    df['date'] = df['startTime'].dt.strftime('%Y-%m-%d')
    df['Year'] = df['startTime'].dt.strftime('%Y')
    df['Month'] = df['startTime'].dt.strftime('%m')
    df['Day'] = df['startTime'].dt.strftime('%d')
    df['Hour'] = df['startTime'].dt.strftime('%H')
    df['Date_Created'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    return(df)
def concat_data(dataframe):
    df = pd.read_csv('Weather_Data.csv')
    df = pd.concat([df,dataframe])
    return(df)
def main():
    #Example Request:  https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}
    apiUrl = f'https://api.weather.gov/gridpoints/LOT/71,80/forecast'
    # Perform the HTTP GET request
    req_data = requests.get(apiUrl)
    req_data_txt = req_data.text
    req_data_txt = req_data_txt.strip()

    df_weather_forcast = parse_data(req_data_txt)
    df_weather_forcast = concat_data(df_weather_forcast)
    df_weather_forcast.to_csv('Weather_Data.csv', index=None)

#    with open('weather.json', 'w') as file:
        #json.dump(df_weather_forcast.to_json(),file)
    # Call the function to handle the API response and display prayer times
    #print(apiUrl,r'\n',req_data.text)


if __name__ == "__main__":
    main()