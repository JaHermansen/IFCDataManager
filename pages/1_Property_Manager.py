import streamlit as st
from tools import ifchelper
from tools import pandashelper
from tools import graph_maker
import pandas as pd
from PIL import Image
import ifcopenshell
import ifcopenshell.util.element as Element
from io import BytesIO
import xlsxwriter
import datetime
from datetime import date
from pathlib import Path
import os
from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.styles import PatternFill
import altair as alt


#Page icon
icon = Image.open('Images/favicon.ico')

st.set_page_config(
    layout= "wide",
    page_title= "IFC Data Manager",
    page_icon= icon,
)




session = st.session_state
# Get the original file name
original_file_name = st.session_state["file_name"]
# Create the updated file name with the current date
updated_file_name = original_file_name.split(".")[0] + "_updated_" + str(date.today()) + ".ifc"



def get_ifc_pandas():
    data, pset_attributes = ifchelper.get_objects_data_by_class(
        session.ifc_file,
        "IfcBuildingElement"
        )
    return ifchelper.create_pandas_dataframe(data, pset_attributes)

def get_ifc_pandas_filter(class_filter):
    data, pset_attributes = ifchelper.get_objects_data_by_class(
        session.ifc_file,
        class_filter
        )
    return ifchelper.create_pandas_dataframe(data, pset_attributes)

def explore():
    # DATA
    st.write("Data:")
    st.write(session.df)  # use df from session_state

def get_df(file):
    # get extension and read file
    extension = file.name.split('.')[1]
    if extension.upper() == 'CSV':
        df = pd.read_csv(file)
    elif extension.upper() == 'XLSX':
        df = pd.read_excel(file, engine='openpyxl')
    elif extension.upper() == 'PICKLE':
        df = pd.read_pickle(file)
    #st.write(f"Debug: {df.head()}")  # debug line
    session.df = df  # store df in session_state

def download_csv():
    pandashelper.download_csv(session.file_name, session.Dataframe)
    
def download_excel():
    pandashelper.download_excel(session.file_name,session.DataFrame)

def callback_upload():
    st.session_state["file_name"] = st.session_state["uploaded_file"].name
    st.session_state["array_buffer"] = st.session_state["uploaded_file"].getvalue()
    st.session_state["is_file_uploaded"] = True


def update_properties(bim_type_codes_selected):

    owner_history = session.ifc_file.by_type("IfcOwnerHistory")[0]
    products = session.ifc_file.by_type("IfcProduct")
    procs = [i for i in products if i.is_a("IfcProduct")]

    for proc in procs:
        property_sets = ifcopenshell.util.element.get_psets(proc)
        property_values = []
        for bim_type_code in bim_type_codes_selected:
            pset_value = None
            for pset_name, properties in property_sets.items():
                for prop_name, prop_values in properties.items():
                    if bim_type_code in prop_name:
                        pset_value = prop_values
                        break
                if pset_value is not None:
                    break

            if pset_value is not None:
                property_values.append(
                    session.ifc_file.createIfcPropertySingleValue(
                        bim_type_code, bim_type_code, session.ifc_file.create_entity("IfcText", str(pset_value)), None
                    )
                )
            else:
                property_values.append(
                    session.ifc_file.createIfcPropertySingleValue(
                        bim_type_code, bim_type_code, session.ifc_file.create_entity("IfcText", "Not Available"), None
                    )
                )
        property_set = session.ifc_file.createIfcPropertySet(proc.GlobalId, owner_history, "Pset_BIMTypeCodes", None, property_values)
        session.ifc_file.createIfcRelDefinesByProperties(proc.GlobalId, owner_history, None, None, [proc], property_set)

    # Write the modified IFC file to a temporary file on disk
    temp_file_path = "temp_updated_file.ifc"
    session.ifc_file.write(temp_file_path)

    # Read the file into a BytesIO object
    updated_file_bytes = BytesIO()
    with open(temp_file_path, 'rb') as f:
        updated_file_bytes.write(f.read())
    updated_file_bytes.seek(0)

    # Optional: Delete the temporary file if it's no longer needed
    os.remove(temp_file_path)

    return updated_file_bytes


def add_new_properties_old(new_properties_dict):
    owner_history = session.ifc_file.by_type("IfcOwnerHistory")[0]
    products = session.ifc_file.by_type("IfcProduct")
    procs = [i for i in products if i.is_a("IfcProduct")]

    for proc in procs:
        identifier = proc.GlobalId  # Get the GlobalId of the current product

        if identifier in new_properties_dict:
            element_properties = new_properties_dict[identifier]
            property_values = []
            for col, values in element_properties.items():
                if "." in col:
                    property_set_name, property_name = col.split(".", 1)
                else:
                    property_set_name = col
                    property_name = col
                property_values.extend(
                    session.ifc_file.createIfcPropertySingleValue(
                        property_name, property_name, session.ifc_file.create_entity("IfcText", str(value)), None
                    )
                    for value in values
                )

            property_set = session.ifc_file.createIfcPropertySet(
                identifier, owner_history, property_set_name, None, property_values
            )
            session.ifc_file.createIfcRelDefinesByProperties(identifier, owner_history, None, None, [proc], property_set)

    # Write the modified IFC file to the Downloads folder
    downloads_path = Path.home() / "Downloads"
    updated_file_path = downloads_path.joinpath(updated_file_name)
    session.ifc_file.write(str(updated_file_path))


def add_new_properties(new_properties_dict):
    owner_history = session.ifc_file.by_type("IfcOwnerHistory")[0]
    products = session.ifc_file.by_type("IfcProduct")
    procs = [i for i in products if i.is_a("IfcProduct")]

    for proc in procs:
        identifier = proc.GlobalId  # Get the GlobalId of the current product

        if identifier in new_properties_dict:
            element_properties = new_properties_dict[identifier]

            for col, values in element_properties.items():
                if "." in col:
                    property_set_name, property_name = col.split(".", 1)
                else:
                    property_set_name = col
                    property_name = col
                
                property_values = []
                for value in values:
                    existing_property = None
                    for prop_set in proc.IsDefinedBy:
                        if (
                            prop_set.is_a("IfcRelDefinesByProperties")
                            and prop_set.RelatingPropertyDefinition.Name == property_set_name
                        ):
                            for prop in prop_set.RelatingPropertyDefinition.HasProperties:
                                if prop.Name == property_name:
                                    existing_property = prop
                                    break
                            if existing_property:
                                break

                    if existing_property:
                        # Update the existing property's value
                        existing_property.NominalValue = session.ifc_file.create_entity("IfcText", str(value))
                    else:
                        # Create a new property
                        property_values.append(
                            session.ifc_file.createIfcPropertySingleValue(
                                property_name, property_name,
                                session.ifc_file.create_entity("IfcText", str(value)), None
                            )
                        )
                
                if property_values:
                    property_set = session.ifc_file.createIfcPropertySet(
                        identifier, owner_history, property_set_name, None, property_values
                    )
                    session.ifc_file.createIfcRelDefinesByProperties(
                        identifier, owner_history, None, None, [proc], property_set
                    )


    # Write the modified IFC file to a temporary file on disk
    tempo_file_path = "tempo_updated_file.ifc"
    session.ifc_file.write(tempo_file_path)

    # Read the file into a BytesIO object
    updated_file = BytesIO()
    with open(tempo_file_path, 'rb') as f:
        updated_file.write(f.read())
    updated_file.seek(0)

    # Optional: Delete the temporary file if it's no longer needed
    os.remove(tempo_file_path)

    return updated_file

def read_data_from_excel(df, sheet_name, global_id_column):
    # Read the sheet with the specified name
    sheet = pd.read_excel(df, sheet_name)

    # Read the IfcBuildingElement objects from the sheet
    ifc_building_elements = session.ifc_file.by_type("IfcBuildingElement")

    # Create a dictionary to store the associated rows of data
    data_dict = {}

    # Iterate over each object in IfcBuildingElement class
    for element in ifc_building_elements:
        global_id = element.GlobalId

        # Find the row in the sheet with the matching GlobalId
        row = sheet[sheet[global_id_column] == global_id]

        # If a matching row is found, store it in the data dictionary
        if not row.empty:
            data_dict[global_id] = row.iloc[0]

    return data_dict

def find_row_with_global_id(df_sheet, global_id):
    row = df_sheet[df_sheet["GlobalId"] == global_id]
    return row.iloc[0] if not row.empty else None

def compare_datasets(df1, df2, identifier_column):
    df1_columns = set(df1.columns)
    df2_columns = set(df2.columns)
    new_columns = df1_columns - df2_columns - {identifier_column}
    return new_columns


def compare_specific_values(df1, df2, specific_columns, identifier_column):
    differing_values_dict = {}  # Dictionary to store differing values by GlobalId

    common_columns = set(specific_columns).intersection(df1.columns).intersection(df2.columns)

    for index, row1 in df1.iterrows():
        global_id = row1[identifier_column]
        row2 = df2[df2[identifier_column] == global_id]

        if not row2.empty:
            differing_props = {}
            for col in common_columns:
                col_name = col.split(".")[-1]
                value1 = row1[col]
                value2 = row2[col].iloc[0]

                if value1 != value2:
                    differing_props[col] = [value2]

            if differing_props:
                differing_values_dict[global_id] = differing_props

    return differing_values_dict


def create_bar_chart(df, selected_columns):
    total_count = len(df)
    filled_counts = df[selected_columns].notna().sum()
    chart_data = pd.DataFrame({
        'Property': selected_columns,
        'Filled Values': filled_counts,
        'Total Rows': total_count
    }).reset_index()
    return chart_data


def execute():
    st.markdown("<h1 style='color: #C0C0C0;'>Model Properties</h1>", unsafe_allow_html=True)
    if st.session_state.get("ifc_file") is None:
        st.warning("No file provided. Please upload a file.")

    else:
        
        tab1, tab2, tab3, tab4 = st.tabs(["Properties Overview", "Property Population", "BIMTypeCodes", "Add External Data"])
        
        with tab1:

            
            st.header("Properties Overview")
            st.write("Overall dataframe")
            # Display the DataFrame
            session_df = st.session_state["DataFrame"]
            if session_df is not None:
                st.write(session_df)
                all_columns = session_df.columns.tolist()

                # Multiselect widget for column filtering
                selected_columns = st.multiselect("Select columns to display", options=all_columns)

                # Filter DataFrame based on selected columns
                if selected_columns:
                    filtered_df = session_df[selected_columns]
                    st.write("Filtered DataFrame:")
                    st.write(filtered_df)
                else:
                    st.warning("Select columns to display")

            else:
                st.warning("DataFrame is not loaded.")


        with tab2:
            st.header("Property Population")
            st.write("Distribution of fulfilled properties")

            # Ensure DataFrame is loaded
            if session_df is not None:
                # Get unique classes from DataFrame
                unique_classes = session_df['Class'].unique()

                # Selectbox to choose class
                selected_class = st.selectbox("Select Class", options=unique_classes)

                # Filter DataFrame by selected class
                df_filtered = session_df[session_df['Class'] == selected_class]

                # Display the filtered DataFrame if desired
                if st.checkbox("Show filtered DataFrame"):
                    st.write(df_filtered)

                # Create a list of all columns
                all_columns = df_filtered.columns.tolist()

                st.markdown(
                    """
                    <style>
                    span[data-baseweb="tag"] {
                        background-color: gray !important;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

                # Multiselect widget for columns to display in the bar chart
                selected_columns = st.multiselect("Select property to display", options=all_columns)

                # Create bar chart for the selected class and columns
                if selected_columns:
                    chart_data = create_bar_chart(df_filtered, selected_columns)

                    base = alt.Chart(chart_data).encode(
                        x=alt.X('Property:N', title='Property')
                    )

                    total_bars = base.mark_bar(opacity=0.5, color='gray').encode(
                        y=alt.Y('Total Rows:Q', title='Amount of objects')
                    )

                    filled_bars = base.mark_bar(opacity=0.7, color='#90EE90').encode(
                        y=alt.Y('Filled Values:Q')
                    )

                    chart = alt.layer(total_bars, filled_bars).resolve_scale(y='shared')

                    # Get current date and file name
                    current_date = datetime.date.today().strftime("%Y-%m-%d")
                    file_name = st.session_state.get("file_name", "Unknown File")

                    # Create the header text
                    header_text = f"Property distribution for {file_name} {selected_class} - {current_date}"

                    # Create a chart for the header
                    header_chart = alt.Chart(pd.DataFrame({'header': [header_text]})).mark_text(
                        align='center',
                        baseline='middle',
                        fontSize=20
                    ).encode(
                        text='header:N'
                    )

                    # Combine the header and the bar chart
                    combined_chart = alt.vconcat(header_chart, chart)

                    st.altair_chart(combined_chart, use_container_width=True)
                else:
                    st.warning("Select columns to display")
            else:
                st.warning("DataFrame is not loaded.")


execute()