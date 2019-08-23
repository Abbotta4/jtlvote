import requests, re
from bs4 import BeautifulSoup

startpost = 584 # https://justthelads.party/mafia/viewtopic.php?p=584#p584
endpost = 646   # https://justthelads.party/mafia/viewtopic.php?p=647#p647

soup_menu = [BeautifulSoup('<html></html', 'html.parser')]
p = startpost
while not soup_menu[-1].find(id='p' + str(endpost)):
    print('fetching: https://justthelads.party/mafia/viewtopic.php?p=' + str(p))
    r = requests.get('https://justthelads.party/mafia/viewtopic.php?p=' + str(p))
    soup = BeautifulSoup(r.content, 'html.parser')
    soup_menu.append(soup)
    pb = soup.find_all(id=re.compile("p\d+"))
    if pb:
        p = int(pb[-1]['id'][1:])
    p += 1

postvotes = {}

for soup in soup_menu:
    pb = soup.find_all(id=re.compile("p\d+"))
    for post in pb:
        if int(post['id'][1:]) >= startpost and int(post['id'][1:]) <= endpost:
            username = post.find(class_=re.compile('username.*')).contents[0].string
            content = post.find(class_='content')
            bolds = content.find_all('strong')
            if bolds:
                for word in bolds:
                    #print(post['id'] + ' ' + username + ' ' +  word.contents[0].string)
                    for person, votes in postvotes.items():
                        if votes[0] is username:
                            votes[2] = False
                    if word.contents:
                        postvotes[word.contents[0].string] = [username, post['id'], True]

print(postvotes)

for person, votes in postvotes:
    
