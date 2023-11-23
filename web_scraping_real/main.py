"""
    pesquisa de emprego
"""

from bs4 import BeautifulSoup
import requests
import csv

print
search_local = input
link_aux = "https://www.net-empregos.com"
job_list = []
html_text = requests.get('https://www.net-empregos.com/pesquisa-empregos.asp?chaves=&cidade=&categoria=0&zona=0&tipo=0').text
soup = BeautifulSoup(html_text, 'lxml')
jobs = soup.find_all('div', class_='job-item media')
jobs_destaque = soup.find_all('div', class_='job-item job-item-destaque media')

all_jobs = list(set(jobs + jobs_destaque))  # com elemento set é garantido que nao existem elementos repetidos

#print("all ", all_jobs)
print("##########################################################################################################")

unique_jobs = set()

for job in all_jobs:
    print(job)
    job_body = job.find('div', class_='media-body align-self-center')
    a_tag = job.find('a', class_='oferta-link')
    if a_tag:
        #link = a_tag.get('href')
        link = link_aux + a_tag.get('href')
        print('link:', link)
        funcao = a_tag.text.strip()
        print("Função:", funcao)
    else:
        print("sem link")
        
    # if job_body:
    #     h2_element = job_body.find('h2')
        
    #     print("elemento", h2_element)
    if job:
        ul_element = job.find('ul')
        if ul_element:
            li_elements = ul_element.find_all('li')
            
            #print("more info:", more_info)
            # Lista de chaves desejadas
            keys_list = ['data', 'local', 'sector', 'nome_empresa', 'link', 'funcao']

            # Criar um dicionário para armazenar os valores
            job_dict = {}

            """Metodo que guarda apenas os registos com informatica"""
            for key, li_element in zip(keys_list, li_elements):
                value = li_element.text.strip()
                print( key, ":", value )
                # Verifica se a chave é 'sector' e se o valor começa com 'Informática'
                if key == 'sector' and not value.startswith('Informática'):
                    # Ignora setores diferentes de 'Informática'
                    continue

                # Ajusta o valor para ser 'Informatica' sem caracteres extras
                if key == 'sector':
                    value = 'Informatica'

                job_dict[key] = value
                job_dict['link'] = link
                job_dict['funcao'] = funcao

            # Verifica se o dicionário contém um setor válido antes de adicionar ao conjunto
            if 'sector' in job_dict:
                unique_jobs.add(tuple(job_dict.items()))

for job_tuple in unique_jobs:
    # Convertendo a tupla de volta para um dicionário para imprimir
    job_dict = dict(job_tuple)
    print(job_dict)

    """ Metodo ok a guardar todos registos"""
    # for key, li_element in zip(keys_list, li_elements):
    #     value = li_element.text.strip()

    #     if key == 'sector' and value.lower().startswith('informática'):
    #         # Ajusta o valor para ser 'Informatica' sem caracteres extras
    #         value = 'Informatica'

    #     job_dict[key] = value
    # # Imprimir o dicionário
    # print(job_dict)
# Abre o arquivo CSV para escrita
with open('lista_empregos.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    # Inicializa o escritor CSV
    writer = csv.writer(csvfile, delimiter=';', lineterminator='\n')

    # Escreve os headers em uma linha
    writer.writerow(job_dict.keys())

    # Escreve os valores correspondentes em colunas separadas
    writer.writerow(job_dict.values())
#else:
    #print("No 'job-ad-item' class found.")
    


    """ codigo ok

    job = soup.find('div', class_= 'job-item media')
    company_tag= job.find('div', class_ = 'job-ad-item') # Local :Lisboa ; Sector: Informática (Programação); Nome Empresa
    # print(company_tag)
    li_elements = company_tag.find('ul').find_all('li')
    #print("elements", li_elements)

    for li_element in li_elements:
        print(li_element.text.strip())

    # Encontrar o elemento <li> com estilo "font-weight:bold" dentro do <ul>
    # company_name = company_tag.find('li', style= 'font-weight:bold').text
    # job_date = company_tag.find('li').text
    # company_local = company_tag.find_next('li').text
    # print(job_date)
    # print("local", company_local)





    # # Obter o texto dentro do elemento
    #company_name = company_element.get_text(strip=True)
    # print(company_name)
    #print(company_local1)
    #print(job)



    """