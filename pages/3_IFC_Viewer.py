import streamlit as st
from PIL import Image

#Page icon
icon = Image.open('Images/favicon.ico')

st.set_page_config(
    layout= "wide",
    page_title= "IFC Data Manager",
    page_icon= icon,
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
