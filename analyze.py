# The Reality Of Mental Health in NYC
# Brought to you by Rakil Ahmed

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_data():
    patient_data = pd.read_csv('patient-data.csv')
    local_data = pd.read_csv('local-data.csv')
    doe_data = pd.read_csv('doe-data.csv')
    return patient_data, local_data, doe_data


def sub_plot(patient_data):
    fig = plt.figure(figsize=(10, 5))
    arr = np.array(patient_data['mental_illness'].value_counts())
    df = pd.DataFrame({'counts': arr}, index=['Yes', 'No'])

    plt.subplot(1, 2, 1)
    plt.bar(df.index, arr, color=['#F5B041', '#138D75'])

    arr2 = np.array(patient_data['age_group'].value_counts())
    df2 = pd.DataFrame({'counts': arr2}, index=['Adult', 'Child'])

    explode = (0.12, 0)
    plt.subplot(1, 2, 2)
    plt.pie(arr2, explode=explode, colors=['#AED6F1', '#FF9999'], labels=df2.index, autopct='%1.1f%%',
            shadow=False, startangle=-10)
    return fig, arr, arr2


def horizontal_bar_graph(patient_data):
    fig = plt.figure(figsize=(10, 2))
    arr = np.array(patient_data['insurance'].value_counts())
    df = pd.DataFrame({'counts': arr}, index=['Yes', 'No'])

    plt.barh(df.index, arr, color=['#48C9B0', '#808B96'])
    plt.xlabel('Number of Patients')
    plt.ylabel('Insurance')
    plt.title('How Many Has Insurance')
    return fig, arr
