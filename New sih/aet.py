import requests
import numpy as np
import pandas as pd

# Function to fetch wind speed
def wind_speed(api_key, lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['wind']['speed']
    else:
        print("Error:", response.status_code, response.text)

# Function to fetch elevation
def get_elevation(lat, lon):
    try:
        url = f"http://api.geonames.org/srtm3?lat={lat}&lng={lon}&username={username}"
        response = requests.get(url)
        response.raise_for_status()
        return float(response.text.strip())  # Ensure elevation is a numeric value
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to estimate net radiation
def estimate_net_radiation(temperature, humidity):
    a = 0.35  # empirical coefficient (unitless)
    b = 0.0025  # empirical coefficient (unitless)
    es = 0.6108 * np.exp((17.27 * temperature) / (temperature + 237.3))  # saturation vapor pressure (Pa)
    ea = (humidity / 100) * es  # actual vapor pressure (Pa)
    net_radiation = (a + b * temperature) * (1 - (ea / es))
    net_radiation_mj = net_radiation * 86400 / 1000000  # Convert to MJ/m²/day
    return net_radiation_mj

# Function to calculate AET
def calculate_aet(net_radiation, temperature, humidity, wind_speed, elevation):
    lambda_v = 2.45  # latent heat of vaporization (MJ/kg)
    rho = 1.2  # air density (kg/m³)
    cp = 1005  # specific heat capacity of air (J/kg/K)
    epsilon = 0.622  # ratio of molecular weight of water vapor to dry air
    es = 0.6108 * np.exp((17.27 * temperature) / (temperature + 237.3))  # saturation vapor pressure (Pa)
    ea = (humidity / 100) * es  # actual vapor pressure (Pa)
    gamma = (cp * rho) / (epsilon * lambda_v)  # Psychrometric constant
    ra = 208 / wind_speed  # Aerodynamic resistance
    rs = 70  # Surface resistance
    aet = (net_radiation * (1 - (ea / es)) + (rho * cp * (es - ea) / ra)) / (lambda_v * (1 + (gamma * (rs + ra)) / (rho * cp)))
    aet_mm_day = aet * 86400 / 1000  # Convert AET to mm/day
    return aet_mm_day

# Input values
api_key = 'Api_Key'
lat = 28.3669
lon = 77.5413
username = '@username'

# Fetch wind speed and elevation
wind_speed_value = wind_speed(api_key, lat, lon)
elevation_value = get_elevation(lat, lon)

# Load dataset
df = pd.read_csv("C://Users//abhin//Desktop//abhinav//New sih//Cleaned_Book1.csv")
df.columns = df.columns.str.strip()


# Add calculated columns
df['net_radiation_direct'] = df.apply(lambda row: estimate_net_radiation(row['temperature(C)'], row['humidity_percent']), axis=1)
df['aet_direct'] = df.apply(
    lambda row: calculate_aet(
        row['net_radiation_direct'],
        row['temperature(C)'],
        row['humidity_percent'],
        wind_speed_value,
        elevation_value
    ), 
    axis=1
)

# Display the updated DataFrame
print(df[['Soil(V/N)', 'temperature(C)', 'humidity_percent', 'water_temp_c', 'net_radiation_direct', 'aet_direct']].head(10))

last_row = df.iloc[-1]
temprature = last_row['temperature(C)']
humidity = last_row['humidity_percent']
windSpeed = wind_speed(api_key=api_key, lat=lat, lon=lon)
elevation = get_elevation(lat=lat,lon=lon)
Net_radiation = estimate_net_radiation(temperature=temprature,humidity=humidity)

print("Wind Speed: ",windSpeed)
print("Elevation: ",elevation)
print("Net Radiation: ",Net_radiation)