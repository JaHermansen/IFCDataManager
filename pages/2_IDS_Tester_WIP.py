from PIL import Image
import streamlit as st

#Page icon
icon = Image.open('Images/favicon.ico')

st.set_page_config(
    layout= "wide",
    page_title= "IFC Data Manager",
    page_icon= icon,
)