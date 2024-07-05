## IFC Data Manager
IFC Data Manager is a Streamlit web application designed to investigate, adjust, and export .ifc files. It allows users to upload .ifc files, analyze IfcProducts, and visualize data distributions.

### Features 
Upload and Load: Upload .ifc files to analyze.
Schema and Metadata: View schema details and project metadata.
IfcProduct Analysis: Count and display IfcProduct entities.
Data Visualization: Visualize IfcProduct distributions using graphs.

## Installation

1. Clone the repository:

git clone https://github.com/your_username/your_repo.git
cd your_repo

2. Install dependencies:
pip install -r requirements.txt

3. Run the Streamlit app:
streamlit run app.py


### Requirements
Python 3.7+
Streamlit
ifcopenshell
altair
pandas
pillow (PIL)
