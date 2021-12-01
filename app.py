# The Reality Of Mental Health in NYC
# Brought to you by Rakil Ahmed

import streamlit as st
import time
import folium
from streamlit_folium import folium_static
import analyze

# Hiding some streamlit elements
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Loading all the csv files
patient_data, local_data, doe_data = analyze.load_data()

# Just to show data is loading up
with st.spinner("Please wait, loading ..."):
    time.sleep(2)

st.title('The Reality of Mental Health in NYC')

with st.expander("Background"):
    st.write("""
    # What is Mental Health?
    *Mental health includes our emotional, psychological, and social well-being. It affects how we think, feel, and act. It also helps determine how we handle stress, relate to others, and make choices. Mental health is important at every stage of life, from childhood and adolescence through adulthood* — Mentalhealth.gov

    # Why is it important to talk about?
    In these unprecedented times, we all are going trhough something whether it is emotinally or financially. And all these unavoidable stress hurting our mental health even if it doesn't seem like it. This is why, we need to talk more about mental health and share as much information as we can to make sure everyone's safe and healthy today, for a better tomorrow.

    *One in five New Yorkers experiences mental illness each year. Hundreds of thousands of these New Yorkers are not connected to care. And hundreds of thousands of these New Yorkers are not connected to care* — NYC Mayor’s Office

    Learn more about mental health [here](https://www.mentalhealth.gov/basics/what-is-mental-health).
    """)

st.subheader('(Survey) Out of 1000, How Many Has Mental Illness?')

# Visuals (bars + pie + explanation)
fig, arr, arr2 = analyze.sub_plot(patient_data)
st.pyplot(fig)
html_str = f"""
<p>To collect this data, 1000 patients were surveyed and {arr[0]} of them (~ {round((arr[0]/1000) * 100, 2)}%) said they have some sort of mental illness and {arr[1]} (~ {round((arr[1]/1000) * 100, 2)}%) said they don't have any. Total {arr2[0]} adults (18 or older) and {arr2[1]} (17 or lower) participated in this survey.</p>
"""
st.markdown(html_str, unsafe_allow_html=True)

fig, arr = analyze.horizontal_bar_graph(patient_data)
st.pyplot(fig)
html_str = f"""
<p>This figure shows about {arr[0]} patients have some sort of health insurance (though, many said it's partially covered, not fully) and unfortunately, {arr[1]} patients don't have any insurance. Although, it may seem like {arr[1]} is not a big number but don't forget this is out of 1000 only. So, that number will increase with the data size.</p>
"""
st.markdown(html_str, unsafe_allow_html=True)

# Maps and dataset details
with st.expander("DOE Services Map"):
    m = folium.Map(location=[doe_data['lat'].mean(),
                             doe_data['lon'].mean()], zoom_start=11, tiles='Stamen Terrain')
    for index, location_info in doe_data.iterrows():
        folium.Marker([location_info["lat"], location_info["lon"]],
                      popup=location_info["address"]).add_to(m)
    folium_static(m)
    st.write(doe_data[['school_name', 'address', 'service']])

with st.expander("Other Local Programs Map"):
    m = folium.Map(location=[local_data['lat'].mean(),
                             local_data['lon'].mean()], zoom_start=6, tiles='Stamen Terrain')
    for index, location_info in local_data.iterrows():
        folium.Marker([location_info["lat"], location_info["lon"]],
                      popup=location_info["address"]).add_to(m)
    folium_static(m)
    st.write(
        local_data[['program_name', 'address', 'program_type_description']])

# Footer
st.write("""
##### Made by [Rakil Ahmed](https://linkedin.com/in/rakil)

##### Learn more about me [here](https://rakilahmed.com) || Thank you :)
""")
