import streamlit as st
import pandas as pd
import geopy
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium

uploaded_file = st.file_uploader("Upload an excel file")
if uploaded_file is not None:
  df = pd.read_excel(uploaded_file)
  df = df.drop(['$Parent','$Address[2].Address','$BillCreditPeriod','$LEDSTATENAME'],axis=1)
  df = df.dropna()
  #st.write(df.shape)
  
  addresses = df['$Address[1].Address'].tolist()
  names = df['$Name'].tolist()

  # Create lists to store the geocoded locations and names
  locations = []
  add_name = []

  # Iterate over the addresses and geocode them
  for (address,name) in zip(addresses,names):
  geolocator = Nominatim(user_agent="my_app", timeout=3)
  location = geolocator.geocode(address)
  if location != None:
    locations.append(location)
    add_name.append(name)

  
  # Create a map centered on first location
  map = folium.Map(location=(locations[0].latitude, locations[0].longitude), zoom_start=12)

  for (location,name) in zip(locations,add_name):
  # Add a marker for  location
  folium.Marker([location.latitude,location.longitude],
                 popup=name).add_to(map)
  
  # Display the map
  st_folium(map, width=700)



  
