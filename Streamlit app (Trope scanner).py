#!/usr/bin/env python
# coding: utf-8

# Importing Streamlit
import streamlit as st

# Function to gracefully exit the app
def exit_app():
    st.stop()

# Main app content
st.title("My Streamlit App")
st.write("Welcome to my first Streamlit app!")

# Add a slider
slider_value = st.slider("Select a value", 0, 100, 50)
st.write(f"You selected: {slider_value}")

# Add an exit button
if st.button("Exit"):
    exit_app()