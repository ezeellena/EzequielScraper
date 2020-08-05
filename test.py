import requests
from bs4 import BeautifulSoup
import re
import json

def filtroReplace(object):
    object.replace("/", "").replace(":", "").replace("%", "").replace("-", "").replace("[", "").replace("]", "").replace("<","").replace(">", "").replace("!", "").replace(",","")
    return " ".join(object.split())

def filtro_tema(j_i, tema):
    c1 = tema.upper() in j_i['desc'].upper()

    if c1:
        r=True
    else:
        r=False
    return r
#j = open("configTagPage.json", "r")
j = open("config1tag.json", "r")
confiTagPage = {}
confiTagPage = json.loads(j.read())["j"]


for urls in confiTagPage:
    url = urls["link"]
    tag = urls["path"]
    noticias = urls["BuscarNoticia"]
    noticias2 = urls["BuscarNoticia2"]
    tema = ""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    response = requests.get(url, headers=headers).text
    items = []

    tmpItems = eval(noticias)
    tmpItems.extend(eval(noticias2))
    url =  url.replace("http:","").replace("//","").replace(".","").replace("www","").replace("https:","").replace("/","").replace("\n","")
    #tag = "i.find("a", {"class": 'link'})['href'].replace(url,"")"
    fic = open("C:/Users/eellena/Desktop/Prueba/"+url+".txt", "w")
    for i in tmpItems:

        try:
            temp9 = ""
            temp10 = ""
            temp11 = ""
            temp12 = ""
            try:
                #print(i.find("h1", {"class": 'titulo'}))
                temp9 = eval(tag)
                temp10 = ""
                temp11 = ""
                temp12 = ""
                url2 = ""
            except:
                try:
                    temp10 = eval(tag2)
                    url2 = ""
                    temp9 = ""
                    temp11 = ""
                    temp12 = ""
                except:
                    try:
                        temp11 = "https://" + re.search('https:\/\/(.*).html', str(i)).group(1) + ".html"
                        url2 = ""
                        temp9 = ""
                        temp12 = ""
                        temp10 = ""
                    except:
                        try:
                            temp12 = "https://" + re.search('https:\/\/(.*)">', str(i)).group(1)
                            url2 = ""
                            temp9 = ""
                            temp11 = ""
                            temp10 = ""
                        except:
                            ulr2 = ""
                            temp11 = ""
                            temp10 = ""
                            temp9 = ""
                            temp12 = ""
                            print(" ********* URL no parseada correctamente: \n", url, "\n")
                            print(i)
                            print("**********************************************************")
            if temp9[:1] == "/":
                temp9 = temp9[1:]
            if "http" in temp9:
                url2 = temp9
                temp9 = ""
            j_i = {"link": url2 + temp9 + temp10 + temp11 + temp12,
                   "desc": filtroReplace(i.get_text()),
                   "tmpItems": i}
            if filtro_tema(j_i, tema):
                # print(j_i['link'])

                fic.write(j_i['link'] +","+ j_i["desc"]+'\n')
                items.append(j_i['link'])
        except Exception as e:
            print("80- for i in tmpItems: ", e)
            print(items)
    fic.close()

