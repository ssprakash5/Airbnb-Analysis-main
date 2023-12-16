import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import matplotlib.pyplot as plt

# Load the Airbnb dataset
airbnb_data = pd.read_csv("C:/Users/Admin/Downloads/Airbnb NYC 2019.csv")

# Convert 'last_review' column to datetime format
airbnb_data['last_review'] = pd.to_datetime(airbnb_data['last_review'], format='%d-%m-%Y')

# Load geospatial data (shapefiles, GeoJSON, etc.) using Geopandas if necessary
geo_data = gpd.read_file("C:/Users/Admin/Downloads/us-states.json")

# Set Streamlit title and sidebar options
st.title("Airbnb Geospatial Visualization")
st.sidebar.header("Filters")

# Create filters for location, price, and other relevant factors
location = st.sidebar.selectbox("Location", airbnb_data['neighbourhood'].unique())
price_range = st.sidebar.slider("Price Range", min_value=0, max_value=1000, step=10, value=(50, 200))
# Add more filters as needed

# Filter the Airbnb dataset based on user selections
filtered_data = airbnb_data[(airbnb_data['neighbourhood'] == location) & (airbnb_data['price'] >= price_range[0]) & (airbnb_data['price'] <= price_range[1])]

# Create an interactive map using Plotly Express
st.header("Interactive Map")
fig = px.scatter_mapbox(
    filtered_data,
    lat="latitude",  # Specify the latitude column
    lon="longitude",  # Specify the longitude column
    color="price",
    size="number_of_reviews",
    text="name",
    mapbox_style="carto-positron",
    zoom=10,
)
st.plotly_chart(fig)

# Display additional information about selected listings
st.header("Selected Listing Details")
# Remove this line as it's not needed: if st.map(fig):
selected_listing = st.selectbox("Select a listing", filtered_data['name'])
details = filtered_data[filtered_data['name'] == selected_listing]
st.write(details)

# Group the data by 'neighbourhood' (place) and create buttons for each place
places = airbnb_data['neighbourhood'].unique()

for place in places:
    if location == place and st.sidebar.button(f"{place}"):
        place_data = airbnb_data[airbnb_data['neighbourhood'] == place]

        room_type = place_data['room_type']
        price = place_data['price']

        st.write(f"{place}")
        fig, ax = plt.subplots()
        ax.bar(room_type, price)
        ax.set_xlabel("Room Type")
        ax.set_ylabel("Price")
        ax.set_title(f"Price vs. Room Type in {place}")
        ax.set_xticklabels(room_type, rotation=45)
        st.pyplot(fig)
