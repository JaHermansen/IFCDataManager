# Streamlit App: IFC Data Manager

## Overview
The IFC Data Manager is a Streamlit-based application designed to manage, explore, and analyze IFC (Industry Foundation Classes) files. It provides functionality for uploading IFC files, exploring their contents, manipulating properties, and visualizing data.

## Homepage
### Features
- Upload and load IFC files.
- Display basic project information like IFC schema and product count.
- Visualize IfcProduct distribution using graphs.

### How to Use
1. Upload an IFC file using the file uploader in the sidebar.
2. Once uploaded, basic project information and product distribution will be displayed.
3. Navigate through different tabs to explore various functionalities.

### Dependencies
- `ifcopenshell`
- `streamlit`
- `PIL`
- `datetime`

## Property Manager
### Features
- Filter and display data from IFC files.
- Modify and update properties of IfcProducts.
- Compare datasets and generate visualizations.

### How to Use
1. Upload an IFC file using the file uploader in the sidebar.
2. Select specific tabs like "Properties Overview" or "Property Population" to explore data.
3. Perform actions like updating properties or comparing datasets as required.

### Dependencies
- `streamlit`
- `ifcopenshell`
- `pandas`
- `altair`
- `openpyxl`

## IFC Viewer
### Features
- Embed an external IFC file viewer using an iframe.
- Allows users to view IFC files externally.

### How to Use
1. Directly embeds an external IFC viewer from a specified source.
2. Provides a seamless viewing experience without leaving the application.

### Dependencies
- `streamlit`
- External IFC viewer source

## Support
For any issues or questions, please contact [your contact information].

## Credits
- Developed using Streamlit and various Python libraries.
- Icons and graphics courtesy of [source].

## License
This application is licensed under [license type].

