import streamlit as st
import pandas as pd
import geopy
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium

uploaded_file = st.file_uploader("Upload an excel file")
if uploaded_file is not None:
  df = pd.read_excel(uploaded_file)
  st.write(df.shape)
  addresses = df['Address'].tolist()
  # Create a list to store the geocoded locations
  locations = []

  # Iterate over the addresses and geocode them
  for address in addresses:
    geolocator = Nominatim(user_agent="my_app", timeout=5)
    location = geolocator.geocode(address)
    if location != None:
      locations.append(location)
  
  # Create a map centered on first location
  map = folium.Map(location=(locations[0].latitude, locations[0].longitude), zoom_start=12)

  for location in locations:  
    # Add a marker for each location
    folium.Marker([location.latitude, location.longitude]).add_to(map)
  
  # Display the map
  st_folium(map)



  
