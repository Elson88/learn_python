### Hands-on lab: Webscraping

from bs4 import BeautifulSoup
import requests
import csv
import sqlite3
import pandas as pd
from requests_html import HTMLSession

url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
db_name = 'Movies.db'
table_name = 'Top_50' 
csv_path = 'top_50_films.csv'
df = pd.DataFrame(columns=["Film", "Year", "Rotten Tomatoes' Top 100"])
count = 0 # como sao necessarios apenas os primeiros 50, é necessario criar um loop

html_page = requests.get(url).text
data = BeautifulSoup(html_page, 'html.parser')


# You now need to write the loop to extract the appropriate information from the web page. 
# The rows of the table needed can be accessed using the find_all() function with the BeautifulSoup object using the statements below.
# The variable tables gets the body of all the tables in the web page and the variable rows gets all the rows of the first table.
tables = data.find_all('tbody')
rows = tables[0].find_all('tr')

for row in rows:                    # Iterate over the contents of the variable 'rows'
    if count < 25:                  # Check for the loop counter to restrict to 50 entries
        col = row.find_all('td')    # Extract all the 'td' data objects in the row and save them to col.
        if len(col) != 0:           # Check if the length of col is 0, that is, if there is no data in a current row. This is important since, many timesm there are merged rows that are not apparent in the web page appearance.
            data_dict = {"Film": col[1].contents[0],
                         "Year": col[2].contents[0], # Create a dictionary data_dict with the keys same as the columns of the dataframe created for recording the output earlier and corresponding values from the first three headers of data.
                         "Rotten Tomatoes' Top 100": col[3].contents[0]}
            df1 = pd.DataFrame(data_dict, index=[0])
            df  = pd.concat([df, df1], ignore_index=True) # Convert the dictionary to a dataframe and concatenate it with the existing one. This way, the data keeps getting appended to the dataframe with every iteration of the loop.
            count+=1                # Increment the loop counter.
    else:
        break                       # Once the counter hits 50, stop iterating over rows and break the loop.
    
print(df[df['Year'].str.startswith('1994')])  # Filter the output to print only the films released in the 2000s (year 2000 included).



# Convert the "Year" column to numeric, and filter for films released in the 2000s
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')  # Convert "Year" to numeric, handle errors
films_in_2000s = df[(df['Year'] >= 2000) & (df['Year'] <= 2009)]

# Print the filtered DataFrame
print(films_in_2000s)
print("\n")
print(df)


# Filter the output to print only the films released in the 2000s (year 2000 included).


### STORING THE DATA

# After the dataframe has been created, you can save it to a CSV file using the following command:

#df.to_csv(csv_path)

# To store the required data in a database, you first need to initialize a connection to the database, save the dataframe as a table, and then close the connection. 
# This can be done using the following code:

# conn = sqlite3.connect(db_name)
# df.to_sql(table_name, conn, if_exists='replace', index=True)
# conn.close()