import streamlit as st
import pandas as pd
import geopy
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium

#App Title
st.header(':blue[Creditor/Debtor Address Mapping] :world_map:', divider='rainbow')

uploaded_file = st.file_uploader("Upload an excel file") #Excel File uploader
  
#Reading the Excel file, storing the name and address columns, dropping the rest 
if uploaded_file is not None:
  df = pd.read_excel(uploaded_file)
  df = df.drop(['$Parent','$Address[2].Address','$BillCreditPeriod','$LEDSTATENAME'],axis=1)
  df = df.dropna()
  st.write("It may take a few minutes. Thank you for your patience!")
  
  addresses = df['$Address[1].Address'].tolist()
  names = df['$Name'].tolist()


  # Create lists to store the geocoded locations and names
  locations = []
  add_name = []

  @st.cache_data # caching decorator, to handle data while reloading
  def load_geodata(addresses,names):
    flag = len(names)#Flag to break the location loop
    i = 1
    with st.spinner('Please wait...'):
    # Iterate over the addresses and geocode them
      for (address,name) in zip(addresses,names):
        geolocator = Nominatim(user_agent="stlit_mapping_app", timeout=10)
        location = geolocator.geocode(address)
        if location != None:
          locations.append(location)
          add_name.append(name)
        i = i + 1
        if i == flag:
          break
    st.success('Interactive Map is ready! Click on marker to display the name.')
    return(locations,add_name)
    
  locations,add_name = load_geodata(addresses,names)
  
  # Create a map centered on first location
  map = folium.Map(location=(locations[0].latitude, locations[0].longitude), zoom_start=12)

  for (location,name) in zip(locations,add_name):
  # Add a marker for location along with popups to display name
    folium.Marker([location.latitude,location.longitude],
                  popup=folium.Popup(f"<h5>{name}<\h5>", max_width=200)).add_to(map)
  
  # Display the map
  st_folium(map, width=1000)
