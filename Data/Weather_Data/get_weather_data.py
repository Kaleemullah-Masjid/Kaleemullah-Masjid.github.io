import pandas as pd
import requests
import datetime
import json

# Function to Request the API
def request_data():
    """
    Requests weather data from the specified API URL.
    Returns: JSON-formatted weather data.
    """
    #Example Request:  https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}
    apiUrl = f'https://api.weather.gov/gridpoints/LOT/71,80/forecast'
    # Perform the HTTP GET request
    req_data = requests.get(apiUrl).text.strip()
    return(req_data)

# Function to parse the JSON data from the API response
def parse_data(response_text):
    """
    Parses JSON-formatted weather data and returns a DataFrame.
    """
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
def concat_data(df):
    """
    Updates the existing DataFrame with new weather data.
    Returns: Updated DataFrame.
    """
    #Open previous dataFrame
    previous_df = pd.read_csv('Data.csv')
    #Identify New Rows from current pull
    new_df = df[~
             (
                 (df.name.isin(previous_df.name))
                & (df.startTime.isin(previous_df.startTime))
                & (df.endTime.isin(previous_df.endTime))              
              )
             ]
    #Combine Old & New Data & Sort Values by Date & Hour
    df = pd.concat([new_df,previous_df]).sort_values(['date','Hour'])

    return(df)
def main():
    """
    Main function to request, parse, and update weather data.
    """
    try:
        #Get New Data 
        req_data = request_data()
        #Parse Json Data
        df_weather_forcast = parse_data(req_data)
        #Combine Old Data with New Data
        df_weather_forcast = concat_data(df_weather_forcast)
        #Export to CSV
        df_weather_forcast.to_csv('Data.csv',index=False)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()