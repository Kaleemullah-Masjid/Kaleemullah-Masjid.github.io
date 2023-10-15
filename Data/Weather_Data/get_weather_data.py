import pandas as pd
import requests
import datetime
import json
from sqlalchemy import create_engine

# Function to Request the API
def request_data():
    #Example Request:  https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}
    apiUrl = f'https://api.weather.gov/gridpoints/LOT/71,80/forecast'
    # Perform the HTTP GET request
    req_data = requests.get(apiUrl).text.strip()
    return(req_data)

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
def concat_data(df):
    #Connect o SQLite database
    engine = create_engine('sqlite:///Weather_Data.db')
    #Set Table Name
    table_name = 'Weather_Forcast'
    # Append DataFrame to the SQLite table
    if not df.empty:
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
    #Commit changes if needed
    engine.dispose()
    return(df)
def main():
    req_data = request_data()
    df_weather_forcast = parse_data(req_data)
    df_weather_forcast = concat_data(df_weather_forcast)


if __name__ == "__main__":
    main()