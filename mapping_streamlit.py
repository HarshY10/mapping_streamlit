import streamlit as st
import pandas as pd
import geopy
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium

st.header(':blue[Creditor/Debtor Mapping] :world_map:', divider='rainbow')
uploaded_file = st.file_uploader("Upload an excel file")
if uploaded_file is not None:
  df = pd.read_excel(uploaded_file)
  df = df.drop(['$Parent','$Address[2].Address','$BillCreditPeriod','$LEDSTATENAME'],axis=1)
  df = df.dropna()
  #st.write(df.shape)
  
  addresses = df['$Address[1].Address'].tolist()
  names = df['$Name'].tolist()

  flag = len(names)#Flag to break the location loop
  i = 1
  
  # Create lists to store the geocoded locations and names
  locations = []
  add_name = []


  with st.spinner('Please wait...'):
    # Iterate over the addresses and geocode them
    for (address,name) in zip(addresses,names):
      geolocator = Nominatim(user_agent="st_mapping_app", timeout=10)
      #geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
      location = geolocator.geocode(address)
      if location != None:
        locations.append(location)
        add_name.append(name)
      i = i + 1
      if i == flag:
        break
  st.success('Map is ready!')
  
  # Create a map centered on first location
  map = folium.Map(location=(locations[0].latitude, locations[0].longitude), zoom_start=12)

  for (location,name) in zip(locations,add_name):
  # Add a marker for  location
    folium.Marker([location.latitude,location.longitude],
                  popup=name).add_to(map)
  
  # Display the map
  st_folium(map, width=700)



  
