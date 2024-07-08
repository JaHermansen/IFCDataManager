import streamlit as st
from PIL import Image
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



def run():
    iframe_src = "https://ifcdm.vercel.app/"

    # Create a container for the iframe and use JavaScript for dynamic resizing
    st.markdown(
        f"""
        <style>
        .iframe-container {{
            position: relative;
            width: 100%;
            height: 100vh; /* 100% of the viewport height */
        }}
        .iframe-container iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 90%;
            border: none;
        }}
        </style>
        <div class="iframe-container">
            <iframe src="{iframe_src}"></iframe>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    run()
