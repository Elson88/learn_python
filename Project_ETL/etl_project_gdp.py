from bs4 import BeautifulSoup
import requests
import csv
import sqlite3
import pandas as pd
from requests_html import HTMLSession
from datetime import datetime

url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
table_attribs = ["Country", "GDP_USD_millions"]
db_name = 'World_Economies.db'
table_name = 'Countries_by_GDP'
csv_path = './Countries_by_GDP.csv'

def extract(url):
    df = pd.DataFrame(columns=["Rank", "Country/Territory", "UN region"])
    html_page = requests.get(url).text
    data = BeautifulSoup(html_page, 'html.parser')
    df = pd.DataFrame(columns=["Country", "GDP_USD_millions"])
    tables = data.find_all('tbody')
    rows = tables[2].find_all('tr')
 
    
    for row in rows:
        col = row.find_all('td')
        if len(col) != 0:
            if col[0].find('a') is not None and '—' not in col[2]:
                data_dict = {"Country": col[0].a.contents[0],
                             "GDP_USD_millions": col[2].contents[0]}
                df1 = pd.DataFrame(data_dict, index=[0])
                df = pd.concat([df,df1], ignore_index=True)
    return df
            
    
#print(extract(url))


def transform(df):
    ''' This function converts the GDP information from Currency
    format to float value, transforms the information of GDP from
    USD (Millions) to USD (Billions) rounding to 2 decimal places.
    The function returns the transformed dataframe.
    
    Save the dataframe column as a list. 
    b. Iterate over the contents of the list and use split() and join() functions to convert the currency text into numerical text. 
    Type cast the numerical text to float.
    '''
     # Apply transformations to the 'GDP_USD_millions' column using the apply function
    # - Use lambda function to remove commas from currency format, convert to float, divide by 1000, and round to 2 decimal places
    df["GDP_USD_billions"] = df["GDP_USD_millions"].apply(lambda x: round(float("".join(x.split(','))) / 1000, 2))
    
    # Rename the column from 'GDP_USD_millions' to 'GDP_USD_billions'
    df = df.rename(columns={"GDP_USD_millions": "GDP_USD_billions"})
    
    
    """
    
    Explanation:

Lambda Function with apply:

df["GDP_USD_millions"].apply(lambda x: round(float("".join(x.split(','))) / 1000, 2)): This line uses the apply function to transform each element in the 'GDP_USD_millions' column.
The lambda function takes an element (x), removes commas from the currency format, converts it to a float, divides by 1000, and rounds to 2 decimal places.
The result is assigned to a new column named 'GDP_USD_billions'.
Column Renaming:

df = df.rename(columns={"GDP_USD_millions": "GDP_USD_billions"}): This line renames the existing column 'GDP_USD_millions' to 'GDP_USD_billions'.
The modified DataFrame is assigned back to the variable df.
Return Statement:

return df: The function returns the modified DataFrame with the transformations applied.
This function now converts the currency format in the 'GDP_USD_millions' column to floating-point numbers, divides the values by 1000, rounds them to 2 decimal places, and renames the column to 'GDP_USD_billions'.

    Returns:
        _type_: _description_
    """
    
    return df

    """
    Metodo curso:
    def transform(df):
    GDP_list = df["GDP_USD_millions"].tolist()
    GDP_list = [float("".join(x.split(','))) for x in GDP_list]
    GDP_list = [np.round(x/1000,2) for x in GDP_list]
    df["GDP_USD_millions"] = GDP_list
    df=df.rename(columns = {"GDP_USD_millions":"GDP_USD_billions"})
    return df

    """

print("transform", transform(extract(url)))



# You have to save the transformed dataframe to a CSV file. 
# For this, pass the dataframe df and the CSV file path to the function load_to_csv() and add the required statements there.
def load_to_csv(df, csv_path):
    df.to_csv(csv_path)
    
# You have to save the transformed dataframe as a table in the database. 
# This needs to be implemented in the function load_to_db(), which accepts the dataframe df, the connection object to the SQL database conn, 
# and the table name variable table_name to be used.
def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)
    
    
""" 
Task 4: Querying the database table
Assuming that the appropriate query was initiated and the query statement has been passed to the function run_query(), 
along with the SQL connection object sql_connection and the table name variable table_name, 
this function should run the query statement on the table and retrieve the output as a filtered dataframe. 
This dataframe can then be simply printed.

"""
def run_query(query_statement, sql_connection):
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)
    
    
    
"""
Task 5: Logging progress
Logging needs to be done using the log_progress() funciton. This function will be called multiple times throughout the execution of this code and will be asked to add a log entry in a .txt file, etl_project_log.txt. The entry is supposed to be in the following format:

'<Time_stamp> : <message_text>'

Here, message text is passed to the function as an argument. Each entry must be in a separate line.
"""
def log_progress(message): 
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open("./etl_project_log.txt","a") as f: 
        f.write(timestamp + ' : ' + message + '\n')
        
        
"""
Function calls
Now, you have to set up the sequence of function calls for your assigned tasks. Follow the sequence below.

Task	Log message on completion
Declaring known values	Preliminaries complete. Initiating ETL process.
Call extract() function	Data extraction complete. Initiating Transformation process.
Call transform() function	Data transformation complete. Initiating loading process.
Call load_to_csv()	Data saved to CSV file.
Initiate SQLite3 connection	SQL Connection initiated.
Call load_to_db()	Data loaded to Database as table. Running the query.
Call run_query() *	Process Complete.
Close SQLite3 connection	-

"""

#Note: The query statement to be executed here is

# f"SELECT * from {table_name} WHERE GDP_USD_billions >= 100"
log_progress('Preliminaries complete. Initiating ETL process')
df = extract(url, table_attribs)
log_progress('Data extraction complete. Initiating Transformation process')
df = transform(df)
log_progress('Data transformation complete. Initiating loading process')
load_to_csv(df, csv_path)
log_progress('Data saved to CSV file')
sql_connection = sqlite3.connect('World_Economies.db')
log_progress('SQL Connection initiated.')
load_to_db(df, sql_connection, table_name)
log_progress('Data loaded to Database as table. Running the query')
query_statement = f"SELECT * from {table_name} WHERE GDP_USD_billions >= 100"
run_query(query_statement, sql_connection)
log_progress('Process Complete.')
sql_connection.close()

