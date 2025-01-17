# Price display with enhanced UI
import streamlit as st
import json
import pickle
import numpy as np

# Utility functions
__locations = None
__data_columns = None
__model = None


def get_estimated_price(location, sqft, bath, bhk):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)


def get_location_names():
    return __locations


def load_saved_artifacts():
    global __data_columns
    global __locations
    global __model

    with open("./artifacts/columns.json", 'r') as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]

    with open("./artifacts/pune_home_prices_model.pickle", 'rb') as f:
        __model = pickle.load(f)


# Load artifacts when the application starts
load_saved_artifacts()

# Streamlit App
st.title("🏠 Pune House Price Prediction")
st.write("Use this app to estimate home prices in Pune based on location, size, and configuration.")

# Sidebar Input Fields
st.sidebar.header("Input Parameters")
locations = get_location_names()
location = st.sidebar.selectbox("Select Location", locations)
total_sqft = st.sidebar.number_input("Total Area (sq.ft)", min_value=100.0, max_value=10000.0, value=1000.0, step=50.0)
bath = st.sidebar.slider("Number of Bathrooms", min_value=1, max_value=10, value=2)
bhk = st.sidebar.slider("Number of BHKs", min_value=1, max_value=10, value=3)

# Enhanced Output Display with Updated Layout
if st.sidebar.button("Predict Price"):
    estimated_price = get_estimated_price(location, total_sqft, bath, bhk)

    # Horizontal Separator
    st.write("---")

    # Full-Width Image
    # st.image(
    #     "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
    #     caption="Your Dream Home Awaits!",
    #     use_container_width=True,
    # )

    # Centered Price and Information
    st.write("###  **Estimated Price**")
    st.markdown(f"## ₹ {estimated_price} Lakhs")

    # Input Summary Details
    st.write(
        """
        **Details:**
        - **Location**: {}
        - **Total Area**: {} sq.ft
        - **Bathrooms**: {}
        - **BHK**: {}
        """.format(location.title(), total_sqft, bath, bhk)
    )

    # Horizontal Separator
    st.write("---")

else:
    st.write("Use the sidebar to enter details and estimate the price.")
