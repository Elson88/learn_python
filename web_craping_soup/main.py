from bs4 import BeautifulSoup

with open('web_craping_soup\home.html','r') as html_file:
    content = html_file.read()
    
    soup = BeautifulSoup(content, 'lxml')
    # print(soup.prettify()) # mostra ficheiro html "bonito e formatado"
    
    
    courser_html_tags = soup.find_all('h5') # find_all encontra todas as tags, assim encontra as repetidas
    
    # metodo para mostrar apenas o texto das tags
    # for course in courser_html_tags:
    #     print(course.text)
    
    # obter o preço dos cursos
    course_cards = soup.find_all('div', class_ = 'card')  # class = class_
    for course in course_cards:
        # print(course.h5) # obtem apenas h5
        course_name = course.h5.text  # optem apenas o texto
        # course_price = course.a.text  # optem apenas o texto
        course_price = course.a.text.split()[-1]  #obtem a ultima string do texto
        print(f'{course_name} costs {course_price}') # "Python for beginners costs 20$"