# The Reality Of Mental Health in NYC
# Brought to you by Rakil Ahmed

# This file reads the already fetched and cleaned datasets and create visuals.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium


def load_data():
    # Reading the fetched datasets
    patient_data = pd.read_csv('patient-data.csv')
    local_data = pd.read_csv('local-data.csv')
    doe_data = pd.read_csv('doe-data.csv')
    return patient_data, local_data, doe_data


def sub_plot(patient_data):
    # Creating & returning the bar and pie charts
    fig = plt.figure(figsize=(10, 5))

    # Bar chart - who has mental illness
    mh_arr = np.array(patient_data['mental_illness'].value_counts())
    mh_df = pd.DataFrame({'counts': mh_arr}, index=['Yes', 'No'])

    plt.subplot(1, 3, 1)
    plt.bar(mh_df.index, mh_arr, color=['#3ae374', '#25CCF7'])
    plt.xticks(rotation=30)

    # Pie chart 1 - Number of adult and children
    age_arr = np.array(patient_data['age_group'].value_counts())
    age_df = pd.DataFrame({'counts': age_arr}, index=['Adult', 'Child'])

    explode = (0.12, 0)
    plt.subplot(1, 3, 2)
    plt.pie(age_arr, explode=explode, colors=['#EAB543', '#55E6C1'], labels=age_df.index, autopct='%1.1f%%',
            shadow=False, startangle=-15)

    # Pie chart 2 - Number of male and female
    sex_arr = np.array(patient_data['sex'].value_counts())
    sex_df = pd.DataFrame({'counts': sex_arr}, index=['Male', 'Female'])

    explode = (0.05, 0)
    plt.subplot(1, 3, 3)
    plt.pie(sex_arr, explode=explode, colors=['#D6A2E8', '#FC427B'], labels=sex_df.index, autopct='%1.1f%%',
            shadow=False, startangle=45)
    return fig, mh_arr, age_arr, sex_arr


def horizontal_bar_graph(patient_data):
    # Creating & returning the horizontal bar chart
    fig = plt.figure(figsize=(10, 2))

    # Horizontal pie chart -
    ins_arr = np.array(patient_data['insurance'].value_counts())
    ins_df = pd.DataFrame({'counts': ins_arr}, index=['Yes', 'No'])

    plt.barh(ins_df.index, ins_arr, color=['#218c74', '#40407a'])
    plt.xlabel('Patients')
    plt.ylabel('Insurance')
    plt.title('Who is covered?')
    plt.yticks(rotation=30)
    return fig, ins_arr


def draw_folium_map(data, zoom, tile):
    map = folium.Map(location=[data['lat'].mean(),
                               data['lon'].mean()], zoom_start=zoom, tiles=tile)
    for index, location_info in data.iterrows():
        folium.Marker([location_info["lat"], location_info["lon"]],
                      popup=location_info["address"], icon=folium.Icon(color='darkblue', icon_color='white', icon='plus')).add_to(map)
    return map
