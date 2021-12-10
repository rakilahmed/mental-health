# The Reality Of Mental Health in NYC
# Brought to you by Rakil Ahmed

import os
from dotenv import load_dotenv
import pandas as pd
from googlemaps import Client as GoogleMaps
import time
import re

# Since I am working with APIs, I am keeping all my keys in a .env file
# load_dotenv() searches for the .env file and loads it into the file
load_dotenv()

# Data URIs and Google API key
GMAPS = GoogleMaps(os.environ.get('API_KEY'))
PATIENT_URI = ('https://data.ny.gov/resource/urn3-ezfe.csv')
LOCAL_URI = ('https://data.ny.gov/resource/6nvr-tbv8.csv')
DOE_URI = ('https://data.cityofnewyork.us/resource/qxbt-vysj.csv')


def fetch_data():
    # Getting the lat and lon using address from Google Geocoding API
    def get_latlon(df):
        df['lat'] = None
        df['lon'] = None
        for x in range(len(df)):
            try:
                time.sleep(1)
                geocode_result = GMAPS.geocode(df['address'][x])
                df['lat'][x] = geocode_result[0]['geometry']['location']['lat']
                df['lon'][x] = geocode_result[0]['geometry']['location']['lng']
            except IndexError:
                print("Address was wrong...")
            except Exception as e:
                print("Unexpected error occurred.", e)
        return df

    # Extracting the lat and lon from the given row
    def extract_latlon(row):
        target = row['georeference']
        pattern = re.compile(r'-[0-9]*\.[0-9]+ [0-9]*\.[0-9]+')
        lat_lon = pattern.findall(target)[0].split(' ')
        return lat_lon[1], lat_lon[0]

    # Cleaning the Patient Survey dataset
    def clean_patient(patient):
        patient = patient[['region_served', 'age_group', 'sex', 'education_status', 'special_education_services',
                           'mental_illness', 'medicaid_insurance']]
        patient = patient.rename(columns={'medicaid_insurance': 'insurance'})
        return patient

    # Cleaning Local Programs dataset
    def clean_local(local):
        local['address'] = local['program_address_1'] + ', ' + \
            local['program_city'] + ', ' + \
            local['program_state'] + ', ' + local['program_zip']
        local = local[['program_name',
                       'program_type_description', 'address', 'georeference']]
        local.dropna(subset=['georeference', 'address'], inplace=True)
        local[['lat', 'lon']] = local.apply(
            extract_latlon, axis=1, result_type='expand')
        return local

    # Cleaning DOE Services dataset
    def clean_doe(doe):
        doe['address'] = doe['primary_address'] + ', ' + \
            doe['city'] + ', ' + 'NY, ' + doe['zip'].apply(str)
        doe = doe[['location_name', 'address', 'service']]
        doe = doe.rename(columns={'location_name': 'school_name'})
        return get_latlon(doe)

    # Calling the URIs and getting csv as response and then cleaning the data
    patient_data = clean_patient(pd.read_csv(PATIENT_URI))
    local_data = clean_local(pd.read_csv(LOCAL_URI))
    doe_data = clean_doe(pd.read_csv(DOE_URI, nrows=10))

    return patient_data, local_data, doe_data


# Fetching the data then writing the cleaned data as csv
patient_data, local_data, doe_data = fetch_data()
patient_data.to_csv('patient-data.csv')
local_data.to_csv('local-data.csv')
doe_data.to_csv('doe-data.csv')
