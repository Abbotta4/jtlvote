import requests, re
from bs4 import BeautifulSoup

startpost = 651 # https://justthelads.party/mafia/viewtopic.php?p=584#p584
endpost = 692   # https://justthelads.party/mafia/viewtopic.php?p=647#p647

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
            for blockquote in content.find_all("blockquote"):
                blockquote.decompose()
            bolds = content.find_all('strong')
            if bolds:
                for word in bolds:
                    if word.contents:
                        for person, votes in postvotes.items():
                            for vote in votes:
                                if vote[0] is username:
                                    vote[2] = False
               
                        if word.contents[0].string not in postvotes.keys():
                            postvotes[word.contents[0].string] = []
                        postvotes[word.contents[0].string].append([username, post['id'], True])

for person, votes in postvotes.items():
    print('Votes for ' + person + ':')
    for vote in votes:
        vote_link = 'https://justthelads.party/mafia/viewtopic.php?p=' + vote[1][1:]
        vote_text = vote[0]
        if not vote[2]:
            vote_text = '[s]' + vote_text + '[/s]'
        vote_text = '[url=' + vote_link + ']' + vote_text + '[/url]'
        print('\t' + vote_text)
    print('')
