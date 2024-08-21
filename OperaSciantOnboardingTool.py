import xml.etree.ElementTree as ET
import pandas as pd
import streamlit as st

# Streamlit app title
st.title("XML Files Data Extractor")

# File uploader
uploaded_files = st.file_uploader("Upload XML files", accept_multiple_files=True, type="xml")

if uploaded_files:
    # List to hold the extracted data
    data = []

    # Process each uploaded XML file
    for uploaded_file in uploaded_files:
        # Parse the XML file
        tree = ET.parse(uploaded_file)
        root = tree.getroot()
        
        # Extract the required fields
        business_date = root.findtext('.//BUSINESS_DATE')
        generation_time = root.findtext('.//GENERATION_TIME')
        from_date = root.findtext('.//FROM_DATE')
        to_date = root.findtext('.//TO_DATE')
        
        # Find the type of EXPORT_HEADER (the tag name under root)
        export_header_type = root.find('.//EXPORT_HEADER').tag
        
        # Store the data in a dictionary
        data.append({
            'BUSINESS_DATE': business_date,
            'GENERATION_TIME': generation_time,
            'FROM_DATE': from_date,
            'TO_DATE': to_date,
            'EXPORT_HEADER_TYPE': export_header_type
        })

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data)

    # Display the DataFrame in Streamlit
    st.write("Extracted Data:")
    st.dataframe(df)
else:
    st.info("Please upload XML files to extract and display data.")
