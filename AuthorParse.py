import pandas as pd
import re

# Load the uploaded files. May need to change path
master_file_path = '/Users/goodman/Desktop/AL_Authors_QGIS/data/Full AL Collection Master File (Updated Aug 13 2024).xlsm'

# Read the master file
master_file = pd.read_excel(master_file_path, sheet_name=None)  # Reading all sheets from the master file

# Cleaning HTML-like tags from the biographies
def clean_biography(text):
    if pd.isna(text):
        return ""
    # Remove HTML tags and unnecessary characters
    clean_text = re.sub(r'<.*?>', '', text)
    clean_text = re.sub(r';|:</strong>|</p>|<br />|</em>|[^\x00-\x7F]+', '', clean_text)
    return clean_text

# Function to search for residence-related keywords in the cleaned biography text
def extract_info(text):
    # Change based on what you're looking for
    info_keywords = ["lived in", "resided", "born in", "moved to", "hometown"]
    text = clean_biography(text)
    
    # Search for residence-related keywords
    for keyword in info_keywords:
        if keyword in text.lower():
            # Extract the sentence or phrase containing the keyword. adjust if the  strings are too long
            start_idx = max(text.lower().find(keyword) - 30, 0)
            end_idx = min(text.lower().find(keyword) + 100, len(text))
            return text[start_idx:end_idx]
    
    return "Alabama, USA"  # Default if no residence info is found

# Extracting the sheet from the master file
master_sheet = master_file['master_new']

# Creating a new dataframe based on the master sheet
parsed_data = {
    "Last_First": master_sheet["Author_Last_Name_First_Name"],
    "First_Last": master_sheet["Author_First_Name_Last_Name"],
    "residence": master_sheet["Author_Biography"].apply(extract_info),
    "Longitude": [],
    "Latitude": []
}

#TODO Code for lat and long here

# Convert parsed data to DataFrame
parsed_df = pd.DataFrame(parsed_data)

# Saving the parsed data with only author and residence to a CSV file
output_csv_path = "/Users/goodman/Desktop/AL_Authors_QGIS/data/Parsed_Author_Data_with_Residences_No_Coordinates.csv"
parsed_df.to_csv(output_csv_path, index=False)

# Display CSV file path
output_csv_path