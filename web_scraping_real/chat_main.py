from bs4 import BeautifulSoup
import requests
import csv

def find_jobs(start_url):
    link_aux = "https://www.net-empregos.com"
    all_jobs = []

    while start_url:
        print('Start_url apos while', start_url)
        html_text = requests.get(start_url).text
        soup = BeautifulSoup(html_text, 'lxml')
        jobs = soup.find_all('div', class_='job-item media')
        jobs_destaque = soup.find_all('div', class_='job-item job-item-destaque media')
        print(jobs)

        all_jobs += process_jobs(link_aux, jobs + jobs_destaque)

        start_url = get_next_page_url(soup)
        print('start url', start_url)
    
    print('all jobs', all_jobs)
    return all_jobs

def process_jobs(link_aux, jobs):
    unique_jobs = set()

    for job in jobs:
        job_body = job.find('div', class_='media-body align-self-center')
        a_tag = job.find('a', class_='oferta-link')
        if a_tag:
            link = link_aux + a_tag.get('href')
            funcao = a_tag.text.strip()
        else:
            continue

        ul_element = job.find('ul')
        if ul_element:
            li_elements = ul_element.find_all('li')

            keys_list = ['data', 'local', 'sector', 'nome_empresa', 'link', 'funcao']
            job_dict = {}

            for key, li_element in zip(keys_list, li_elements):
                value = li_element.text.strip()

                if key == 'sector' and not value.startswith('Informática'):
                    continue

                if key == 'sector':
                    value = 'Informatica'

                job_dict[key] = value
                job_dict['link'] = link
                job_dict['funcao'] = funcao

            if 'sector' in job_dict:
                unique_jobs.add(tuple(job_dict.items()))

    return [dict(job_tuple) for job_tuple in unique_jobs]

def get_next_page_url(soup):
    page = soup.find('ul', {'class': 'pagination'})
    if page:
        next_page_link = page.find('a', {'class': 'page-link oferta-link d-none d-lg-block', 'rel': 'next'})
        if next_page_link and 'href' in next_page_link.attrs:
            url_next = 'https://www.net-empregos.com' + next_page_link['href']
            return url_next
    return None

# Exemplo de utilização:
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