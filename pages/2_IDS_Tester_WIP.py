from PIL import Image
import streamlit as st
import base64

#Page icon
icon = Image.open('Images/favicon.ico')

st.set_page_config(
    layout= "wide",
    page_title= "IFC Data Manager",
    page_icon= icon,
)


# Function to load and encode image to base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Path to your background image
background_path = 'Images/background.jpg'
background_ext = 'jpg'

# Encode the image to base64
background_base64 = get_base64_of_bin_file(background_path)

# Apply the background image using CSS
st.markdown(
    f"""
    <style>
    .stApp {{
        background: url(data:image/{background_ext};base64,{background_base64});
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
