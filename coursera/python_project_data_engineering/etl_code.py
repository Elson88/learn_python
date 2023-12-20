import glob 
import pandas as pd 
import xml.etree.ElementTree as ET 
from datetime import datetime 


log_file = "log_file.txt" 
target_file = "transformed_data.csv" 


# To extract from a CSV file, you can define the function extract_from_csv()as follows using the pandas function read_csv:
def extract_from_csv(file_to_process):
    dataframe = pd.read_csv(file_to_process)
    return dataframe

# To extract from a JSON file, you can define the function extract_from_json()using the pandas function read_json. 
# It requires an extra argument lines=True to enable the function to read the file as a JSON object on line to line basis as follows.

def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process, lines=True)
    return dataframe





# To extract from an XML file, you need first to parse the data from the file using the ElementTree function. 
# You can then extract relevant information from this data and append it to a pandas dataframe as follows.

# Note: You must know the headers of the extracted data to write this function. 
# In this data, you extract "name", "height", and "weight" headers for different persons.

def extract_from_xml(file_to_process):
    # Create an empty DataFrame with columns: "name", "height", "weight"
    dataframe = pd.DataFrame(columns=['name', 'height', 'weight'])
    
    # Parse the XML file and get the root of the XML tree
    tree = ET.parse(file_to_process)
    root = tree.getroot()
    
    # Iterate over each "person" element in the XML
    for person in root:
        # Extract the "name" from the current "person" element
        name = person.find('name').text
        # Extract the "height" from the current "person" element and convert it to a float
        height = float(person.find('height').text)
        # Extract the "weight" from the current "person" element and convert it to a float
        weight = float(person.find('weight').text)

        # Create a temporary DataFrame with the current person's data and concatenate it to the main DataFrame
        dataframe = pd.concat([dataframe, pd.DataFrame([{'name': name, 'height': height, 'weight': weight }])], ignore_index=True)
    # Return the final DataFrame containing all the extracted data from the XML file
    return dataframe



# Now you need a function to identify which function to call on basis of the filetype of the data file. 
# To call the relevant function, write a function extract, which uses the glob library to identify the filetype.

"""
    This function is designed to process CSV, JSON, and XML files in the current directory. 
    It uses helper functions (extract_from_csv, extract_from_json, and extract_from_xml) to extract data from each file type and then 
    concatenates the results into a single DataFrame. 
"""
def extract():
    # Create an empty DataFrame to hold the extracted data with columns: 'name', 'height', 'weight'
    extracted_data = pd.DataFrame(columns=['name', 'height', 'weight'])

    # Process all CSV files in the current directory
    for csvfile in glob.glob("*.csv"):
        # Extract data from the CSV file using the extract_from_csv function and concatenate it to the main DataFrame
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_csv(csvfile))], ignore_index=True)

    # Process all JSON files in the current directory
    for jsonfile in glob.glob("*.json"):
        # Extract data from the JSON file using the extract_from_json function and concatenate it to the main DataFrame
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_json(jsonfile))], ignore_index=True)

    # Process all XML files in the current directory
    for xmlfile in glob.glob("*.xml"):
        # Extract data from the XML file using the extract_from_xml function and concatenate it to the main DataFrame
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_xml(xmlfile))], ignore_index=True)

    # Return the final DataFrame containing all the extracted data from CSV, JSON, and XML files
    return extracted_data

"""
    
Task 2 - Transformation

The height in the extracted data is in inches, and the weight is in pounds. 

However, for your application, the height is required to be in meters, and the weight is required to be in kilograms, rounded to two decimal places. 

-Therefore, you need to write the function to perform the unit conversion for the two parameters.

-The name of this function will be transform(), and it will receive the extracted dataframe as the input. 

-Since the dataframe is in the form of a dictionary with three keys, "name", "height", and "weight", each of them having a list of values, 
you can apply the transform function on the entire list at one go.

The output of this function will now be a dataframe where the "height" and "weight" parameters will be modified to the required format.
"""

def transform(data): 
    '''Convert inches to meters and round off to two decimals 
    1 inch is 0.0254 meters '''
    data['height'] = round(data.height * 0.0254,2) 
 
    '''Convert pounds to kilograms and round off to two decimals 
    1 pound is 0.45359237 kilograms '''
    data['weight'] = round(data.weight * 0.45359237,2) 
    
    return data 



"""
Task 3 - Loading and Logging

-You need to load the transformed data to a CSV file that you can use to load to a database as per requirement.

-To load the data, you need a function load_data() that accepts the transformed data as a dataframe and the target_file path. 

-You need to use the to_csv attribute of the dataframe in the function:


-This function takes a DataFrame (transformed_data) and a target file name (target_file) as input, 
and it saves the DataFrame to a CSV file using the to_csv method. 
-The to_csv method writes the DataFrame to a CSV file with the specified file name (target_file). 


"""

def load_data(target_file, transformed_data):
    # Save the transformed data DataFrame to a CSV file with the specified target file name
    transformed_data.to_csv(target_file)
    
    
"""
Finally, you need to implement the logging operation to record the progress of the different operations. 

-For this operation, you need to record a message, along with its timestamp, in the log_file.

- To record the message, you need to implement a function log_progress() that accepts the log message as the argument. 

-The function captures the current date and time using the datetime function from the datetime library. 
-The use of this function requires the definition of a date-time format, 
and you need to convert the timestamp to a string format using the strftime attribute. 

Explain:
-This function logs progress by appending a timestamp and a message to a log file. 
-It uses the datetime module to get the current timestamp, formats it according to the specified format, and 
then writes the timestamp and message to a new line in the log file specified by the variable log_file

"""

def log_progress(message):
    # Define the timestamp format as 'Year-Monthname-Day-Hour-Minute-Second'
    timestamp_format = '%Y-%h-%d-%H:%M:%S'

    # Get the current timestamp
    now = datetime.now()

    # Format the current timestamp using the specified format
    timestamp = now.strftime(timestamp_format)

    # Open the log file in append mode and write the timestamp and message to a new line
    with open(log_file, "a") as f:
        f.write(timestamp + ',' + message + '\n')
        
        
        
        
##########             Testing ETL operations and log progress 

# Log the initialization of the ETL process 
log_progress("ETL Job Started") 
 
# Log the beginning of the Extraction process 
log_progress("Extract phase Started") 
extracted_data = extract() 
 
# Log the completion of the Extraction process 
log_progress("Extract phase Ended") 
 
# Log the beginning of the Transformation process 
log_progress("Transform phase Started") 
transformed_data = transform(extracted_data) 
print("Transformed Data") 
print(transformed_data) 
 
# Log the completion of the Transformation process 
log_progress("Transform phase Ended") 
 
# Log the beginning of the Loading process 
log_progress("Load phase Started") 
load_data(target_file,transformed_data) 
 
# Log the completion of the Loading process 
log_progress("Load phase Ended") 
 
# Log the completion of the ETL process 
log_progress("ETL Job Ended") 