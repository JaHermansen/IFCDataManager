import ifcopenshell
import streamlit as st
from PIL import Image
from tools import ifchelper
from tools import graph_maker
import datetime

# Page icon
icon = Image.open('Images/favicon.ico')

def callback_upload():
    st.session_state["file_name"] = st.session_state["uploaded_file"].name
    st.session_state["array_buffer"] = st.session_state["uploaded_file"].getvalue()
    st.session_state["ifc_file"] = ifcopenshell.file.from_string(st.session_state["uploaded_file"].getvalue().decode("utf-8"))
    st.session_state["is_file_uploaded"] = True
    # Create the DataFrame and store it in the session state
    data, pset_attributes = ifchelper.get_objects_data_by_class(st.session_state["ifc_file"], "IfcBuildingElement")
    st.session_state["DataFrame"] = ifchelper.create_pandas_dataframe(data, pset_attributes)

def get_project_name():
    return st.session_state.get("file_name", "")

def remove_uploaded_file():
    st.session_state["file_name"] = ""
    st.session_state["array_buffer"] = None
    st.session_state["ifc_file"] = None
    st.session_state["is_file_uploaded"] = False


def count_ifc_products(ifc_file):
    project = ifc_file
    products = project.by_type("IfcProduct")
    count = len(products)
    return count

def get_file_creation_date(ifc_file_path):
    ifc_file = ifc_file_path
    owner_history = ifc_file.by_type("IfcOwnerHistory")[0]
    creation_date = owner_history.CreationDate
    date_time = datetime.datetime.fromtimestamp(creation_date)
    formatted_date = date_time.strftime("%Y-%m-%d ")
    return formatted_date

def main():
    # Initialize session state variables
    if "file_name" not in st.session_state:
        st.session_state["file_name"] = ""
    if "array_buffer" not in st.session_state:
        st.session_state["array_buffer"] = None
    if "ifc_file" not in st.session_state:
        st.session_state["ifc_file"] = None
    if "is_file_uploaded" not in st.session_state:
        st.session_state["is_file_uploaded"] = False

    st.set_page_config(
        layout="wide",
        page_title="IFC Data Manager",
        page_icon=icon,
    )
    st.markdown("<h1 style='color: #C0C0C0;'>IFC Data Manager</h1>", unsafe_allow_html=True)
    st.markdown(
        """ 
        #####  Investigate, adjust, and export .ifc files
        """
    )
    st.markdown("""---""")


    uploaded_file = st.sidebar.file_uploader("Choose a file", key="uploaded_file", on_change=callback_upload)
    if st.sidebar.button("Remove File"):
        remove_uploaded_file()

    if st.session_state["is_file_uploaded"]:
        st.sidebar.success("Project successfully loaded")
        
    if st.session_state["file_name"] != "":
        col1, col2 = st.columns(2)

        if st.session_state["ifc_file"] is None:
            st.warning("No file provided. Please upload a file.")
        else:
            with col1:
                st.markdown("##### Project resume")
                st.write("IFC schema: " + "".join(str(item) for item in st.session_state["ifc_file"].schema))
                st.write(f"Project name: {get_project_name()}")
                # creation_date = get_file_creation_date(st.session_state["ifc_file"])
                # st.write("Creation Date: " + str(creation_date))
                product_count = count_ifc_products(st.session_state["ifc_file"])
                st.write("##### IfcProducts")
                st.write("IfcProducts entities: " + str(product_count))


            with col2:
                st.markdown("#### IfcProduct distribution")
                graph = graph_maker.get_elements_graph(st.session_state["ifc_file"])
                st.write(graph)


if __name__ == "__main__":
    main()
