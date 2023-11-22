import requests

# payload = {'page': 2 , 'count':25} # get parameters na lista, assim nao é necessario colocar no url
# r = requests.get('https://httpbin.org/get', params=payload)
# print(r.url) # 

#print(dir(r))  # atributes and methods
#print(help(r))

# obter a imagem/content
# r = requests.get('https://imgs.xkcd.com/comics/python.png')
# print(r.content) # obtem os bytes


# cria e escreve os bytes obtidos no r.content para o novo ficheiro, cria png
# with open('comic.png', 'wb') as f:
#   f.write(r.content)


# if resposta/status cod
# print(r.status_code)
# print(r.ok)
# print(r.headers)


####### POST

#payload = {'username': 'corey' , 'password':'testing'} # get parameters na lista, assim nao é necessario colocar no url
# r = requests.post('https://httpbin.org/post', data=payload)
# print(r.text) # 

## COMO É DEVOLVIDO UM JSON:
# print(r.json())
# Quando queremos apanhar algum objecto. 1º colocamos numa lista
#r_dict = r.json()

# obtem o couteudo dentro da key form: {'password': 'testing', 'username': 'corey'}
#print(r_dict['form'])


######## AUTHENTICATION


#r = requests.get('https://httpbin.org/basic-auth/corey/testing', auth=('corey', 'testing')) # auth: user, pw
# Timeout: 
r = requests.get('https://httpbin.org/delay/5', timeout=3) # auth: user, pw

print(r)






