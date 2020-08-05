import json
import pickle
import urllib
import numpy as np
from bs4 import BeautifulSoup
import requests
import re
import os
def save_persist(elem):
    try:
        vpath = directorio+"persist/"

        varchivo = vpath + elem + ".bin"
        with open(varchivo, "bw") as archivo:
            pickle.dump(eval(elem), archivo)
    except Exception as e:

        print("Except de save_persist", e)

def load_persist(elem):

    try:

        vpath = directorio+"persist/"
        varchivo = vpath + elem + ".bin"

        with open(varchivo, "br") as archivo:
            # #print(pickle.load(archivo))
            return pickle.load(archivo)

    except Exception as e:

        print("269 - Except load_persit ", e)


class RSSParser( object ):
    def parse(self,url,tag,noticias, fic, tema):
        items = []
        #OBTENGO EL HTML COMPLETO
        #response = requests.get(url).text

        #OBTENGO TODAS LAS ETIQUETAS "ARTICLE" (ES el estandar que encontre para todas las noticias)
        #tmpItems = BeautifulSoup(response, "lxml").find_all("div", {"class": re.compile('penci-item-mag penci(.*?)')})

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
            }
            response = requests.get(url, headers=headers).text
        except Exception as e:
            response = urllib.request.urlopen(url).read()

        tmpItems = eval(noticias)

        #url3 = url3.replace("http:", "").replace("//", "").replace(".", "").replace("www", "").replace("https:","").replace("/","").replace("\n", "")
        #fic = open("C:/Users/eellena/Desktop/Prueba/" + url3 + ".txt", "w")
        for i in tmpItems:

            try:
                temp9 = ""
                temp10 = ""
                temp11 = ""
                temp12 = ""
                try:
                    # print(i.find("h1", {"class": 'titulo'}))
                    temp9 = eval(tag)
                    temp10 = ""
                    temp11 = ""
                    temp12 = ""
                    url2 = url
                except:
                    try:
                        temp10 = i.a["href"]
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

                    fic.write(j_i['link'] + "," + j_i["desc"] + '\n')
                    items.append(j_i['link'])
            except Exception as e:
                print("80- for i in tmpItems: ", e)
                print(items)
        return items


def filtroReplace(object):
    object.replace("/", "").replace(":", "").replace("%", "").replace("-", "").replace("[", "").replace("]", "").replace("<","").replace(">", "").replace("!", "").replace(",","")
    return " ".join(object.split())

def filtro_repetida(j_i):
    dd = j_i['desc']
    #dd = dd.replace("/", "").replace(":", "").replace("%", "").replace("-", "").replace("[", "").replace("]", "").replace("<", "").replace(">", "").replace("!", "").replace("\n","")

    print(dd)
    r = False
    if dd in db_noticias2.keys():
        if (db_noticias2[dd] == 1):
            r = True
        else:
            r= False
    if not r:
        db_noticias2[dd] = 1
        save_persist('db_noticias2')
    return r

def filtro_tema(j_i, tema):
    c1 = tema.upper() in j_i['desc'].upper()

    if c1:
        r=True
    else:
        r=False
    return r


a_url_temas = []


def enviar_noticias(arr):


    try:
        url_api = token + "/sendMessage"

        print( "- tema \n", Tema, " \n ",  NombreGrupo )
        men_t = "✔ Noticias referidas al tema %s, enviadas al grupo de télegram %s: " % (Tema,NombreGrupo) + "\n"
        ta = False
        # recorro el arreglo de links y lo imprimos
        men = []
        print("arr \n",  arr)
        print( "men_t \n", men_t )
        for a in arr:
            print("3- ",a)
            #men += "- " + a + "\n\n"

            # armo la linea
            l = "- " + a + "\n\n"
            men.append(l)
            if a != "":
                ta = True
        if ta:
            # Si tiene información, mando el título.
            requests.post( 'https://api.telegram.org/' + url_api, data={'chat_id': idchat, 'text': men_t} )
            for m in men:
                requests.post( 'https://api.telegram.org/' + url_api, data={'chat_id': idchat, 'text': '\n [' + NombreGrupo + ']\n' + m} )
                print(requests.status_codes)
    except Exception as e:
        print(" 279 - enviar ",e)


def configuracion():
    f = open("config.json", "r")

    global j_config
    j_config = {}
    j_config = json.loads(f.read())
    global token
    token = j_config["token"]
    global idchat
    idchat = j_config["id_chat"]
    global Tema
    Tema = j_config["Tema"]
    global NombreGrupo
    NombreGrupo = j_config["NombreGrupo"]
    global directorio
    directorio = j_config["directorio"]
    try:
        global db_noticias2

        db_noticias2 = {}

        if os.path.isfile(directorio +'persist/db_noticias2.bin'):
            db_noticias2 = load_persist("db_noticias2")
        else:
            db_noticias2 = {}


    except:

        db_noticias2 = {}
if __name__ == "__main__":
    configuracion()

    fic = open(directorio + "Log.txt", "r+")
    #ABRO EL ARCHIVO DONDE SE ENCUENTRAN LOS LINKS DE LAS PAGINAS WEBS
    #try:
        #links = open(directorio + "links.txt", "r", encoding='utf-8-sig')
        #for ff in links:
            #print(ff)
            #a_url_temas.append(ff)
    #except Exception as e:
        #print(e)
    #ITERO CADA UNA DE LAS URL

    j = open("config1tag.json", "r")
    confiTagPage = {}
    confiTagPage = json.loads(j.read())["j"]

    for urls in confiTagPage:
        url = urls["link"]
        tag = urls["path"]
        noticias = urls["BuscarNoticia"]
        if url != "":
            r = RSSParser().parse(url,tag,noticias, fic, Tema)
            if r != []:
                enviar_noticias(r)
        #ENVIO LAS NOTICIAS A TELEGRAM
    #CIERRO EL TXT
    fic.close()
