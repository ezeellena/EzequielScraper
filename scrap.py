import datetime
import json
import pickle
import urllib
import requests
import re
import os
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options as FirefoxOptions
j_link_enviado = {}

j_pag_ne = {}

mugre = ["xmlns=http://www.w3.org/1999/>", "<\n", "\n>", "<<p>", "<p>", "</p", "xmlns=http://www.w3.org/1999/>",
         "xmlns=http://www.w3.org/1999/>", "<br />", "CDATA", "</div>>", "<div>", "</div>", "%>", "<iframe>",
         "</iframe>", "100%", "<div", "http://w3.org/", "xmlms", "xhtml", ";>", "<", ">", "'", '"', "\/", "]", "["]


def limpiar(texto, mugre):
    for m in mugre:
        texto = texto.replace(m, "")
    return texto


def link_enviado(l):
    l = limpiar(l, mugre)
    if not l in j_link_enviado.keys():
        print(" Enviando a telegram :", l)
        j_link_enviado[l] = 1
        return False
    else:
        print(" !!!!!!!!!!!!!!! ENCONTRO DUPLICADO !!!!!!!!!!!!!!!!!! ")
        return True


def log(texto):
    l = open("log.csv", "a")
    l.write(texto + "\n")
    l.close()


def save_persist(elem):
    try:
        vpath = "./persist/"

        varchivo = vpath + elem + ".bin"
        with open(varchivo, "bw") as archivo:
            pickle.dump(eval(elem), archivo)
    except Exception as e:

        print("Except de save_persist", e)


def load_persist(elem):
    try:

        vpath = "./persist/"
        varchivo = vpath + elem + ".bin"

        with open(varchivo, "br") as archivo:
            # #print(pickle.load(archivo))
            return pickle.load(archivo)

    except Exception as e:

        print("269 - Except load_persit ", e)


class RSSParser(object):
    def parse(self, urlytag, fic, tema):
        items = []
        url = urlytag["link"]
        urlCortada = urlytag["link"]
        tag = urlytag["path"]
        try:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
                }
                response = requests.get(url, headers=headers).text
            except Exception as e:
                response = urllib.request.urlopen(url).read()
        except Exception as e:
            print(" 58 - response ", e)

        tmpItems = eval(urlytag["BuscarNoticia"])
        if urlytag["BuscarNoticia2"] != "":
            noticias2 = eval(urlytag["BuscarNoticia2"])
            tmpItems.extend(eval(noticias2))
        urlCortada = urlCortada.replace("http:", "").replace("//", "").replace(".", "").replace("www", "").replace(
            "https:", "").replace("/", "").replace("\n", "")
        fic = open("C:/Users/eellena/Desktop/Prueba/" + urlCortada + ".txt", "w")

        ficComparativo = open("C:/Users/eellena/Desktop/Prueba/" + urlCortada + "LOG.txt", "w", encoding='utf-8')
        for i in tmpItems:

            try:
                temp9 = ""

                temp10 = ""

                temp11 = ""

                temp12 = ""

                try:
                    temp8 = eval(tag)
                    temp9 = eval(tag)

                    temp10 = ""
                    temp11 = ""
                    temp12 = ""
                    url2 = url


                except:
                    # si falla el eval, forma el ínice de esta manera

                    try:
                        temp10 = re.search('href="(.*)">', str(i)).group(1)
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

                                if not i.text in j_pag_ne.keys():
                                    j_pag_ne[i.text] = 1
                                    log("***** \n No scrapeó esta página: \n" + url + '\n' + str(
                                        i) + '\n ********')

                """
                print("- url: ", url)
                print("- temp9:" , temp9)
                print("--------------------------------")

                """

                if temp9[:1] == "/":
                    temp9 = temp9[1:]

                if "http" in temp9:
                    url2 = temp9
                    temp9 = ""

                # print(" url final:  ", url +  temp9 + temp10 + temp11, "\n temp9: ", temp9, "\n temp10: ",temp10, "\n temp11: ",temp11, "\n temp12: ",temp12)

                j_i = {"link": url2 + temp9 + temp10 + temp11 + temp12,
                       "desc": filtroReplace(i.get_text()),
                       "tmpItems": i}
                if not filtro_repetida(j_i):
                    if filtro_tema(j_i, tema):
                        link_noticia = url + temp8.replace(url, "")
                        link_web = urlytag["link"]
                        response2 = requests.get(link_noticia, headers=headers).text
                        #driver.get(link_noticia)

                        FechaHoraScrapeo = str(datetime.datetime.now())
                        try:
                            titulo_noticia = eval(urlytag["tituloNoticia"])
                        except Exception as e:
                            print(e)
                            try:
                                titulo_noticia = eval(urlytag["tituloNoticia2"])
                            except Exception as e:
                                print(e)
                                titulo_noticia = "No se pudo obtener el titulo de la noticia"
                        try:
                            DescripcionNoticia = eval(urlytag["descripcionNoticia"])
                        except Exception as e:
                            print(e)
                            try:
                                DescripcionNoticia = eval(urlytag["descripcionNoticia2"])
                            except Exception as e:
                                print(e)
                                DescripcionNoticia = "No se pudo obtener la descripcion de la noticia"
                        try:
                            Nota = eval(urlytag["Nota"])
                            NotComp = ""
                            if type(Nota) != str:
                                for no in Nota:
                                    NotComp += no.text
                                Nota = NotComp
                        except Exception as e:
                            print(e)
                            try:
                                Nota = eval(urlytag["Nota2"])
                            except Exception as e:
                                print(e)
                                Nota = "No se pudo obtener la nota"
                        try:
                            fechaPublicacion = eval(urlytag["fechaPublicacion"])
                        except Exception as e:
                            print(e)
                            try:
                                fechaPublicacion = eval(urlytag["fechaPublicacion2"])
                            except Exception as e:
                                print(e)
                                fechaPublicacion = "No se pudo obtener fecha de publicacion"
                        try:
                            fechaPublicacionModificacion = eval(urlytag["fechaPublicacionModificada"])
                        except Exception as e:
                            print(e)
                            try:
                                fechaPublicacionModificacion = eval(urlytag["fechaPublicacionModificada2"])
                            except Exception as e:
                                print(e)
                                fechaPublicacionModificacion = "No se pudo obtener fecha de modificacion"

                        data = {"Pagina_Web": link_web,
                                "Link_Noticia": link_noticia,
                                "Fecha_Hora_Scrapeo": FechaHoraScrapeo,
                                "Fecha_Hora_Noticia": fechaPublicacion,
                                "Fecha_Modificacion": fechaPublicacionModificacion,
                                "Titulo_Noticia": titulo_noticia,
                                "Descripcion_Noticia:": DescripcionNoticia,
                                "Texto_Noticia": Nota.replace("\n", "")}
                        stringjsonordenado = json.dumps(data, indent=4, sort_keys=False, ensure_ascii=False)
                        print(stringjsonordenado)
                        ficComparativo.write(stringjsonordenado + '\n')
                        fic.write(link_noticia + '\n')
                        items.append(link_noticia)
            except Exception as e:
                print(e)
        ficComparativo.close()
        return items


def filtroReplace(object):
    object.replace("/", "").replace(":", "").replace("%", "").replace("-", "").replace("[", "").replace("]", "").replace("<","").replace(
        ">", "").replace("!", "").replace(",", "")
    return " ".join(object.split())


def filtro_repetida(j_i):
    dd = j_i['link'].replace("\n", "")[1:250]

    if "reconquista" in dd:
        print("parar")

    dd = limpiar(dd, mugre)
    # dd = dd.replace("/", "").replace(":", "").replace("%", "").replace("-", "").replace("[", "").replace("]", "").replace("<", "").replace(">", "").replace("!", "").replace("\n","")

    # print(dd)
    r = False
    if dd in db_noticias2.keys():
        if (db_noticias2[dd] == 1):
            r = True
        else:
            r = False
    if not r:
        db_noticias2[dd] = 1
        save_persist('db_noticias2')
    return r


def filtro_tema(j_i, tema):
    c1 = tema.upper() in j_i['desc'].upper()

    if c1:
        r = True
    else:
        r = False
    return r


a_url_temas = []


def init():
    global vtelegram
    vtelegram = True

    def get_config(vkey):
        c = vkey in j_config.keys()
        if c:
            return j_config[vkey]
        else:
            return '-1'


def enviar_noticias(arr):
    if not vtelegram:
        pass
        # return

    try:
        url_api = token + "/sendMessage"

        # print( "- tema \n", Tema, " \n ",  NombreGrupo )
        men_t = "✔ Noticias referidas al tema %s, enviadas al grupo de télegram %s: " % (Tema, NombreGrupo) + "\n"
        ta = False
        # recorro el arreglo de links y lo imprimos
        men = []
        # print("arr \n",  arr)
        # print( "men_t \n", men_t )
        for a in arr:
            # print("3- ",a)
            # men += "- " + a + "\n\n"

            # armo la linea
            l = "- " + a + "\n\n"
            men.append(l)
            if a != "" and not (link_enviado(a)):
                ta = True
        if ta:
            # Si tiene información, mando el título.
            requests.post('https://api.telegram.org/' + url_api, data={'chat_id': idchat, 'text': men_t})
            for m in men:
                requests.post('https://api.telegram.org/' + url_api,
                              data={'chat_id': idchat, 'text': '\n [' + NombreGrupo + ']\n' + m})
                print(requests.status_codes)
    except Exception as e:
        print(" 279 - enviar ", e)


def configuracion():
    f = open("config.json", "r")

    global j_config
    j_config = {}
    j_config = json.loads(f.read())

    global vtelegram

    try:
        vtelegram = j_config["telegram"]
    except:
        vtelegram = True

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

        if os.path.isfile(directorio + 'persist/db_noticias2.bin'):
            db_noticias2 = load_persist("db_noticias2")
        else:
            db_noticias2 = {}


    except:

        db_noticias2 = {}


if __name__ == "__main__":
    configuracion()
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("browser.download.folderList", 2)
    firefox_profile.set_preference("javascript.enabled", False)

    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    fic = open(directorio + "Log.txt", "r+")

    j = open("configParaIngresarAlLink.json", "r")
    confiTagPage = {}
    confiTagPage = json.loads(j.read())["j"]

    while True:
        try:

            for url in confiTagPage:
                if url != "":

                    print(" Procesando la url:  ", url)

                    r = RSSParser().parse(url, fic, Tema)
                    if r != []:
                        enviar_noticias(r)
        except Exception as e:
            print("207 - problema en el for general ", e)
    fic.close()
