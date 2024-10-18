import pandas as pd
import re

# Load the uploaded files
# TODO CHANGE THIS TO YOUR PATH
master_file_path = '/Users/goodman/Desktop/AL_Authors_QGIS/data/Full AL Collection Master File (Updated Aug 13 2024).xlsm'

# Read the master file
master_file = pd.read_excel(master_file_path, sheet_name=None)

# Hardcoded dictionary of Alabama cities with their respective latitude and longitude
# TODO CHANGE ADD LOCATIONS YOU NEED
alabama_city_coordinates = {
    "Birmingham": (33.5186, -86.8104),
    "Montgomery": (32.3792, -86.3077),
    "Mobile": (30.6954, -88.0399),
    "Huntsville": (34.7304, -86.5861),
    "Tuscaloosa": (33.2098, -87.5692),
    "Auburn": (32.6099, -85.4808),
    "Hoover": (33.4054, -86.8114),
    "Dothan": (31.2232, -85.3905),
    "Decatur": (34.6059, -86.9833),
    "Florence": (34.7998, -87.6773),
    "Opelika": (32.6454, -85.3783),
    "Gadsden": (34.0143, -86.0066),
    "Anniston": (33.6598, -85.8316),
    "Prattville": (32.4640, -86.4597),
    "Phenix City": (32.4700, -85.0007),
    "Vestavia Hills": (33.4487, -86.7878),
    "Alabaster": (33.2443, -86.8164),
    "Bessemer": (33.4018, -86.9544),
    "Enterprise": (31.3152, -85.8552),
    "Athens": (34.8029, -86.9717),
    "Pelham": (33.2859, -86.8097),
    "Madison": (34.6993, -86.7483),
    "Selma": (32.4074, -87.0211),
    "Foley": (30.4069, -87.6836),
    "Gulf Shores": (30.2460, -87.7008),
    "Fairhope": (30.5229, -87.9033),
    "Cullman": (34.1748, -86.8436),
    "Scottsboro": (34.6723, -86.0341),
    "Jasper": (33.8318, -87.2775),
    "Talladega": (33.4359, -86.1000),
    "Sylacauga": (33.1732, -86.2503),
    "Eufaula": (31.8918, -85.1455),
    "Ozark": (31.4590, -85.6400),
    "Troy": (31.8088, -85.9699),
    "Alexander City": (32.9440, -85.9539),
    "Millbrook": (32.4790, -86.3619),
    "Trussville": (33.6198, -86.6089),
    "Northport": (33.2290, -87.5772),
    "Saraland": (30.8207, -88.0703),
    "Helena": (33.2962, -86.8439),
    "Clanton": (32.8387, -86.6294),
    "Boaz": (34.2001, -86.1522),
    "Fort Payne": (34.4443, -85.7194),
    "Monroeville": (31.5274, -87.3247),
    "Andalusia": (31.3088, -86.4836),
    "Demopolis": (32.5174, -87.8369),
    "Oneonta": (33.9487, -86.4722)
    # TODO Add all cities/ locations
    # You can continue to add more cities as necessary
}

# Function to clean biography text
def clean_biography(text):
    if pd.isna(text):
        return ""
    clean_text = re.sub(r'<.*?>', '', text)
    clean_text = re.sub(r';|:</strong>|</p>|<br />|</em>|[^\x00-\x7F]+', '', clean_text)
    return clean_text

# Function to search for residence-related keywords in the cleaned biography text
def extract_info(text):
    # TODO EDIT KEYWORDS TO FIND WHAT YOU NEED
    info_keywords = ["Education", "studied in"]
    text = clean_biography(text)
    
    for keyword in info_keywords:
        if keyword in text.lower():
            start_idx = max(text.lower().find(keyword) - 30, 0)
            end_idx = min(text.lower().find(keyword) + 100, len(text))
            return text[start_idx:end_idx]
    
    return "NOT FOUND"

# Extract the sheet from the master file
master_sheet = master_file['master_new']

# Creating a new dataframe based on the master sheet
parsed_data = {
    "Last_First": master_sheet["Author_Last_Name_First_Name"],
    "First_Last": master_sheet["Author_First_Name_Last_Name"],
    "info": master_sheet["Author_Biography"].apply(extract_info),
}

# Convert parsed data to DataFrame
parsed_df = pd.DataFrame(parsed_data)

# Alabama cities list (you can extend this list as needed)
alabama_cities = list(alabama_city_coordinates.keys())

# Function to find if an Alabama city is mentioned in the residence text
def find_city(text):
    for city in alabama_cities:
        # Look for city name in the residence text
        if city.lower() in text.lower():
            return city
    return None

# Function to get the hardcoded latitude and longitude for the city
def get_lat_long(city):
    if city in alabama_city_coordinates:
        return alabama_city_coordinates[city]
    return None, None

# Populate latitude and longitude columns based on the city mentioned in info
parsed_df['city'] = parsed_df['info'].apply(find_city)
parsed_df['latitude'], parsed_df['longitude'] = zip(*parsed_df['city'].apply(get_lat_long))

#filter incomplete rows
filtered_df = parsed_df.dropna(subset=['latitude', 'longitude'])
# Saving the parsed data with author names, info, and lat/long fields to a CSV file
# TODO CHANGE PATH TO WHERE YOUR OUTPUT WILL GO
output_csv_path = "/Users/goodman/Desktop/AL_Authors_QGIS/data/TestCSV.csv"
filtered_df.to_csv(output_csv_path, index=False)

# Create a second DataFrame for rows that are missing latitude and longitude
missing_lat_long_df = parsed_df[parsed_df['latitude'].isna() | parsed_df['longitude'].isna()]

# Save the rows missing lat/long to a second CSV file
# TODO CHANGE PATH TO WHERE YOUR OUTPUT WILL GO
output_csv_path_missing = "/Users/goodman/Desktop/AL_Authors_QGIS/data/missing.csv"
missing_lat_long_df.to_csv(output_csv_path_missing, index=False)

# Display CSV file path
(output_csv_path, output_csv_path_missing)