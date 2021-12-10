# The Reality Of Mental Health in NYC
# Brought to you by Rakil Ahmed

# This file takes everything and uses Streamlit.io library to create a visual dashboard for the user

import streamlit as st
import time
from streamlit_folium import folium_static
from PIL import Image
import visualize

# Loading all the csv files
patient_data, local_data, doe_data = visualize.load_data()

# Loading the data
with st.spinner("Please wait, loading ..."):
    time.sleep(2)

# Setting the title and image side-by-side
left_col, right_col = st.columns(2)
with left_col:
    st.write("""
    # The Reality of Mental Health in NYC
    ### By: Rakil Ahmed
    **[LinkedIn] (https://linkedin.com/in/rakil) | [Website] (https://rakilahmed.com) | [GitHub] (https://github.com/rakilahmed) | [Source Code] (https://github.com/rakilahmed/mental-health)**
    """)
with right_col:
    image = Image.open('mental-health.png')
    st.image(image)

# Overview of the project
with st.expander("Background"):
    st.write("""
    ### Abstract

    The purpose of this project is to raise awareness about mental health and ways to get help if needed. 
    Also, this project shed some light on health insurance and how bad the system unfortunately is. 
    It visualizes the data and make it easy for the user to see the bigger picture and really understand the issue.

    ### What is Mental Health?

    Mental health includes our emotional, psychological, and social well-being. 
    It affects how we think, feel, and act. It also helps determine how we handle stress, relate to others, and make choices. 
    Mental health is important at every stage of life, from childhood and adolescence through adulthood.

    ### Why is it important to talk about?

    In these unprecedented times, we all are going through something whether it is emotinally or financially. 
    And all these unavoidable stress hurting our mental health even if it doesn't seem like it. 
    This is why, we need to talk more about mental health and share as much information 
    as we can to make sure everyone's safe and healthy **TODAY**, for a better **TOMORROW**.

    - One in five New Yorkers experiences mental illness each year. 
    Hundreds of thousands of these New Yorkers are not connected to care. 
    - Hundreds of thousands of these New Yorkers are not connected to care.

    Learn more about **Mental Health** [here] (https://www.mentalhealth.gov/basics/what-is-mental-health).
    """)

# Details of the datasets
with st.expander("Data"):
    st.write("""
    ### Dataset 1 - Patient Characteristics Survey (2019)

    The data for this dataset was collected from a month long survey which was organized by OMH. 
    It contains the patient's responses to each question in separate columns. 
    Before cleaning, it had around 76 columns with a lot of information but for the simplicity of this project, I ended up using only 6 columns.

    ### Dataset 2 - 2020-21 SMH Service Coverage

    This dataset conatins a list of DOE schools which provides mental health services. 
    It has all the school names, location, and the type of service(s) they provide. 
    It is meant to be a snapshot of mental health service coverage in DOE schools and it was organized by the NYC Department of Eductaion. 

    ### Dataset 3 - Local Mental Health Programs

    Similar to the second dataset, it contains a list of local places where mental health services are available. 
    This dataset contains programs that are licensed and funded by the Office of Mental Health.
    """)

# Tools & techniques used to build the project
with st.expander("Tools & Techniques"):
    st.write("""
    ### Tools

    - Language — ***Python (v3.9.8)***
    - Libraries — ***Pandas*** | ***NumPy*** | ***Matplotlib*** | ***Folium***
    - Third Party Libs — ***Streamlit*** | ***GoogleMaps***

    ### Techniques

    First I called each dataset's API then fetch & read the data as csv. 
    Then I called few cleaning functions which I defined earlier, to modify each dataset for further analysis. 
    One of my datasets was missing the **Latitude** & **Longitude** columns. 
    So, I decided to use the **GoogleMaps** API to generate the **lat** & **lon** columns for each location.
    After that, I used **Pandas** and **NumPy** to analyze the cleaned data and visualize them using **Matplotlib** and **Folium**.
    Finally, I used **Streamlit** to create this dashboard with all the important information and visuals for the user. 
    """)

# Visuals (bars + pie + explanation)
# Visual 1
st.subheader('(Survey) Who Has Mental Illness?')
figure_1, mh_arr, age_arr, sex_arr = visualize.sub_plot(patient_data)
st.pyplot(figure_1)
html_str = f"""
<p>To collect this data, 1000 patients were surveyed and <strong>{mh_arr[0]}</strong> of them <strong>(~ {round((mh_arr[0]/1000) * 100, 2)}%)</strong> 
said they have some sort of mental illness and <strong>{mh_arr[1]} (~ {round((mh_arr[1]/1000) * 100, 2)}%)</strong> said they don't have any. 
Total <strong>{age_arr[0]}</strong> adults and <strong>{age_arr[1]}</strong> children (<strong>{sex_arr[0]}</strong> male & <strong>{sex_arr[1]}</strong> female) participated in this survey.</p>
"""
st.markdown(html_str, unsafe_allow_html=True)

# Visual 2
figure_2, ins_arr = visualize.horizontal_bar_graph(patient_data)
st.pyplot(figure_2)
html_str = f"""
<p>This figure shows about <strong>{ins_arr[0]}</strong> patients <strong>(~ {round((ins_arr[0]/1000) * 100, 2)}%)</strong> have some sort of 
health insurance (though, many said it's partially covered, not fully) and unfortunately, 
<strong>{ins_arr[1]}</strong> patients <strong>(~ {round((ins_arr[1]/1000) * 100, 2)}%)</strong> don't have any insurance. 
It may seem like <strong>{ins_arr[1]}</strong> is not a big number but don't forget this is out of <strong>1000</strong> only. 
So, that number will likely increase with the data size.</p>
"""
st.markdown(html_str, unsafe_allow_html=True)

# Maps and dataset details
# Map 1
with st.expander("DOE Services Map"):
    map = visualize.draw_folium_map(
        data=doe_data, zoom=12, tile='Stamen Terrain')
    folium_static(map)
    st.write(doe_data[['school_name', 'address', 'service']])

# Map 2
with st.expander("Other Local Programs Map"):
    map = visualize.draw_folium_map(
        data=local_data, zoom=7, tile='Stamen Terrain')
    folium_static(map)
    st.write(
        local_data[['program_name', 'address', 'program_type_description']])

# Resources used to build the project
with st.expander("Citations"):
    st.write("""
    ### Datasets

    - [Patient Characteristics Survey (2019)] (https://data.ny.gov/Human-Services/Patient-Characteristics-Survey-PCS-2019/urn3-ezfe)
    - [Local Mental Health Programs] (https://data.ny.gov/Human-Services/Local-Mental-Health-Programs/6nvr-tbv8)
    - [2020-21 SMH Service Coverage] (https://data.cityofnewyork.us/Education/2020-21-SMH-Service-Coverage/qxbt-vysj)

    ### Articles

    - [What Is Mental Health?] (https://www.mentalhealth.gov/basics/what-is-mental-health)
    - [CDC - About Mental Health] (https://www.cdc.gov/mentalhealth/learn/index.htm)
    - [NYC Mayor's Office - Mental Health] (https://mentalhealth.cityofnewyork.us/dashboard/?q=34964534045)
    """)

# Hiding some streamlit elements
hide_streamlit_style = """
     <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
