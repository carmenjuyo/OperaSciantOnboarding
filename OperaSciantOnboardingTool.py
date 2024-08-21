import xml.etree.ElementTree as ET
import pandas as pd
import streamlit as st

# Set Streamlit page configuration to wide mode
st.set_page_config(layout="wide")

# Streamlit app title
st.title("XML Files Data Extractor")

# Display max upload size info (assumed 1000 MB)
max_upload_size_mb = 1000  # This should match the value in your config.toml
st.info(f"Maximum upload size per file: {max_upload_size_mb} MB")

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
        export_header_element = root.find('.//EXPORT_HEADER')
        export_header_type = export_header_element.tag
        
        # Extract the first 5 characters following the <EXPORT_HEADER> tag
        following_text = export_header_element.tail.strip() if export_header_element.tail else ""
        first_5_characters = following_text[:5]
        
        # Store the data in a dictionary, including the file name and first 5 characters
        data.append({
            'Source File': uploaded_file.name,
            'BUSINESS_DATE': business_date,
            'GENERATION_TIME': generation_time,
            'FROM_DATE': from_date,
            'TO_DATE': to_date,
            'EXPORT_HEADER_TYPE': export_header_type,
            'First 5 Chars After EXPORT_HEADER': first_5_characters
        })

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data)

    # Ensure the columns are in a fixed order
    df = df[['Source File', 'BUSINESS_DATE', 'GENERATION_TIME', 'FROM_DATE', 'TO_DATE', 'EXPORT_HEADER_TYPE', 'First 5 Chars After EXPORT_HEADER']]

    # Display the DataFrame in Streamlit with a wide frame
    st.write("Extracted Data:")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Please upload XML files to extract and display data.")
