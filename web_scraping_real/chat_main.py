import requests
from bs4 import BeautifulSoup
import csv

def find_jobs(start_url):
    # Base URL for constructing complete job links
    link_aux = "https://www.net-empregos.com"
    # List to store all job information
    all_jobs = []

    # Loop until there are no more pages
    while start_url:
        print('Start_url after while:', start_url)
        # Fetch HTML content from the current page
        html_text = requests.get(start_url).text
        soup = BeautifulSoup(html_text, 'lxml')
        # Find job items on the page
        jobs = soup.find_all('div', class_='job-item media')
        jobs_destaque = soup.find_all('div', class_='job-item job-item-destaque media')

        # Process job information and add to the list
        all_jobs += process_jobs(link_aux, jobs + jobs_destaque)

        # Get the URL of the next page
        start_url = get_next_page_url(soup)
        print('Next start_url:', start_url)
    
    print('All jobs:', all_jobs)
    return all_jobs

def process_jobs(link_aux, jobs):
    # Set to store unique jobs based on their information
    unique_jobs = set()

    for job in jobs:
        # Extract relevant elements from the job
        job_body = job.find('div', class_='media-body align-self-center')
        a_tag = job.find('a', class_='oferta-link')

        # If 'a' tag is present, extract additional information
        if a_tag:
            link = link_aux + a_tag.get('href')
            funcao = a_tag.text.strip()
        else:
            continue

        # Extract additional job details from 'ul' element
        ul_element = job.find('ul')
        if ul_element:
            li_elements = ul_element.find_all('li')

            # Define keys for job details
            keys_list = ['data', 'local', 'sector', 'nome_empresa', 'link', 'funcao']
            job_dict = {}

            # Extract values and populate the dictionary
            for key, li_element in zip(keys_list, li_elements):
                value = li_element.text.strip()

                # Skip non-Informatica sectors
                if key == 'sector' and not value.startswith('Informática'):
                    continue

                # Replace sector value to 'Informatica'
                if key == 'sector':
                    value = 'Informatica'

                job_dict[key] = value
                job_dict['link'] = link
                job_dict['funcao'] = funcao

            # Check if 'sector' key exists before adding to unique_jobs
            if 'sector' in job_dict:
                unique_jobs.add(tuple(job_dict.items()))

    # Convert unique_jobs set to a list of dictionaries
    return [dict(job_tuple) for job_tuple in unique_jobs]

def get_next_page_url(soup):
    # Find the URL of the next page
    page = soup.find('ul', {'class': 'pagination'})
    if page:
        next_page_link = page.find('a', {'class': 'page-link oferta-link d-none d-lg-block', 'rel': 'next'})
        if next_page_link and 'href' in next_page_link.attrs:
            url_next = 'https://www.net-empregos.com' + next_page_link['href']
            return url_next
    return None

# Example usage:
start_url = 'https://www.net-empregos.com/pesquisa-empregos.asp?page=1&categoria=0&zona=0&tipo=0'
result = find_jobs(start_url)
print(result)

# def save_to_file(result):
#     with open('lista_empregos.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
#             # Inicializa o escritor CSV
#             writer = csv.DictWriter(csvfile, fieldnames=result[0].keys(), delimiter=';', lineterminator='\n')

#             # Escreve os headers em uma linha
#             writer.writeheader()

#             # Escreve cada linha de dados no arquivo
#             writer.writerows(result)

# save_to_file(result)